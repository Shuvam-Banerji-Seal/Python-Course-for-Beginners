import tkinter as tk
from tkinter import ttk, messagebox
import requests
import sqlite3
import hashlib
import random
import html

DB_NAME = "quiz_users.db"
AUTHOR = "Niket Basu"

# --- Database functions ---
def setup_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True
    return False

def update_score(username, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET score = score + ? WHERE username = ?", (score, username))
    conn.commit()
    conn.close()

def get_user_score(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT score FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def get_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return rows

# --- API Interaction ---
def fetch_categories():
    url = "https://opentdb.com/api_category.php"
    data = requests.get(url).json()
    categories = {cat['name']: cat['id'] for cat in data['trivia_categories']}
    return categories

def fetch_questions(amount, category, difficulty, qtype):
    url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "category": category,
        "difficulty": difficulty,
        "type": qtype
    }
    data = requests.get(url, params=params).json()
    return data['results']

# --- Main Application ---
class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Master - By Niket Basu")
        self.geometry("850x600")
        self.resizable(False, False)
        self.configure(bg="#293462")
        setup_db()
        self.username = None
        self.frames = {}
        self.show_frame(LoginFrame)

    def show_frame(self, frame_class, **kwargs):
        frame = self.frames.get(frame_class)
        if not frame:
            frame = frame_class(self, **kwargs)
            self.frames[frame_class] = frame
        frame.tkraise()

    def logout(self):
        self.username = None
        self.show_frame(LoginFrame)

# --- Login/Signup ---
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#293462")
        self.place(relwidth=1, relheight=1)
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 16), padding=6)
        tk.Label(self, text="Quiz Master", font=("Arial Rounded MT Bold", 40, "bold"), bg="#293462", fg="#FFF").pack(pady=30)
        frm = tk.Frame(self, bg="#293462")
        frm.pack()
        tk.Label(frm, text="Username:", font=("Arial", 16), bg="#293462", fg="#FFF").grid(row=0, column=0, sticky="e", pady=5)
        tk.Label(frm, text="Password:", font=("Arial", 16), bg="#293462", fg="#FFF").grid(row=1, column=0, sticky="e", pady=5)
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.username_var, font=("Arial", 16)).grid(row=0, column=1, pady=5)
        ttk.Entry(frm, textvariable=self.password_var, font=("Arial", 16), show="*").grid(row=1, column=1, pady=5)
        btn_frm = tk.Frame(self, bg="#293462")
        btn_frm.pack(pady=10)
        ttk.Button(btn_frm, text="Login", command=self.login).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frm, text="Sign Up", command=self.signup).grid(row=0, column=1, padx=10)
        self.info_lbl = tk.Label(self, text="", font=("Arial", 14), bg="#293462", fg="#FFD700")
        self.info_lbl.pack(pady=10)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if validate_user(username, password):
            self.master.username = username
            self.master.show_frame(HomeFrame)
        else:
            self.info_lbl.config(text="Invalid username or password.")

    def signup(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if register_user(username, password):
            self.info_lbl.config(text="Registration successful! Please login.")
        else:
            self.info_lbl.config(text="Username already exists.")

# --- Home Screen ---
class HomeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#293462")
        self.place(relwidth=1, relheight=1)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Welcome, {self.master.username}!", font=("Arial Rounded MT Bold", 26, "bold"), bg="#293462", fg="#FFF").pack(pady=25)
        score = get_user_score(self.master.username)
        tk.Label(self, text=f"Your Score: {score}", font=("Arial", 20), bg="#293462", fg="#FFD700").pack()
        tk.Label(self, text="Choose Quiz Settings", font=("Arial", 16), bg="#293462", fg="#FFF").pack(pady=15)
        categories = fetch_categories()
        self.category_var = tk.StringVar(value=list(categories.keys())[0])
        self.amount_var = tk.IntVar(value=10)
        self.difficulty_var = tk.StringVar(value="medium")
        self.type_var = tk.StringVar(value="multiple")
        frm = tk.Frame(self, bg="#293462")
        frm.pack(pady=10)
        ttk.Label(frm, text="Category:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(frm, textvariable=self.category_var, values=list(categories.keys()), state="readonly", width=30).grid(row=0, column=1)
        ttk.Label(frm, text="Number of Questions:").grid(row=1, column=0, sticky="w")
        ttk.Spinbox(frm, from_=5, to=50, textvariable=self.amount_var, width=5).grid(row=1, column=1)
        ttk.Label(frm, text="Difficulty:").grid(row=2, column=0, sticky="w")
        ttk.Combobox(frm, textvariable=self.difficulty_var, values=["easy", "medium", "hard"], state="readonly", width=10).grid(row=2, column=1)
        ttk.Label(frm, text="Type:").grid(row=3, column=0, sticky="w")
        ttk.Combobox(frm, textvariable=self.type_var, values=["multiple", "boolean"], state="readonly", width=10).grid(row=3, column=1)
        ttk.Button(self, text="Start Quiz", command=lambda: self.start_quiz(categories)).pack(pady=15)
        ttk.Button(self, text="Leaderboard", command=self.show_leaderboard).pack(pady=5)
        ttk.Button(self, text="Logout", command=self.master.logout).pack(pady=5)

    def start_quiz(self, categories):
        category_id = categories[self.category_var.get()]
        amount = self.amount_var.get()
        difficulty = self.difficulty_var.get()
        qtype = self.type_var.get()
        questions = fetch_questions(amount, category_id, difficulty, qtype)
        if not questions:
            messagebox.showerror("Error", "No questions found. Try different settings!")
            return
        self.master.show_frame(QuizFrame, questions=questions)

    def show_leaderboard(self):
        self.master.show_frame(LeaderboardFrame)

# --- Quiz Frame ---
class QuizFrame(tk.Frame):
    def __init__(self, master, questions):
        super().__init__(master, bg="#293462")
        self.place(relwidth=1, relheight=1)
        self.questions = questions
        self.q_index = 0
        self.score = 0
        self.selected = tk.StringVar()
        self.show_question()

    def show_question(self):
        for widget in self.winfo_children():
            widget.destroy()
        if self.q_index < len(self.questions):
            q = self.questions[self.q_index]
            question = html.unescape(q["question"])
            tk.Label(self, text=f"Q{self.q_index+1}. {question}", font=("Arial", 18), wraplength=750, bg="#293462", fg="#FFF").pack(pady=30)
            answers = [html.unescape(ans) for ans in q.get("incorrect_answers", [])]
            answers.append(html.unescape(q["correct_answer"]))
            random.shuffle(answers)
            self.selected.set(None)
            for ans in answers:
                ttk.Radiobutton(self, text=ans, value=ans, variable=self.selected, style='TButton').pack(anchor="w", padx=80, pady=5)
            ttk.Button(self, text="Submit", command=self.check_answer).pack(pady=30)
        else:
            update_score(self.master.username, self.score)
            tk.Label(self, text=f"Quiz Finished!\nYour Score: {self.score}/{len(self.questions)}", font=("Arial", 22, "bold"), bg="#293462", fg="#FFD700").pack(pady=60)
            ttk.Button(self, text="Back to Home", command=lambda: self.master.show_frame(HomeFrame)).pack(pady=15)
            ttk.Button(self, text="View Leaderboard", command=lambda: self.master.show_frame(LeaderboardFrame)).pack(pady=5)

    def check_answer(self):
        q = self.questions[self.q_index]
        correct = html.unescape(q["correct_answer"])
        chosen = self.selected.get()
        if not chosen:
            messagebox.showwarning("Select an answer", "Please select an answer before submitting.")
            return
        if correct == chosen:
            self.score += 1
            messagebox.showinfo("Correct!", "That's the right answer!")
        else:
            messagebox.showinfo("Wrong!", f"Correct answer was: {correct}")
        self.q_index += 1
        self.show_question()

# --- Leaderboard Frame ---
class LeaderboardFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#293462")
        self.place(relwidth=1, relheight=1)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Leaderboard", font=("Arial Rounded MT Bold", 28, "bold"), bg="#293462", fg="#FFD700").pack(pady=30)
        leaderboard = get_leaderboard()
        frm = tk.Frame(self, bg="#293462")
        frm.pack()
        tk.Label(frm, text="Rank", font=("Arial", 18, "bold"), width=8, bg="#293462", fg="#FFF").grid(row=0, column=0)
        tk.Label(frm, text="Username", font=("Arial", 18, "bold"), width=16, bg="#293462", fg="#FFF").grid(row=0, column=1)
        tk.Label(frm, text="Score", font=("Arial", 18, "bold"), width=10, bg="#293462", fg="#FFF").grid(row=0, column=2)
        for idx, (username, score) in enumerate(leaderboard, 1):
            tk.Label(frm, text=str(idx), font=("Arial", 16), width=8, bg="#293462", fg="#FFD700").grid(row=idx, column=0)
            tk.Label(frm, text=username, font=("Arial", 16), width=16, bg="#293462", fg="#FFF").grid(row=idx, column=1)
            tk.Label(frm, text=str(score), font=("Arial", 16), width=10, bg="#293462", fg="#FFF").grid(row=idx, column=2)
        ttk.Button(self, text="Back", command=lambda: self.master.show_frame(HomeFrame)).pack(pady=20)

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()