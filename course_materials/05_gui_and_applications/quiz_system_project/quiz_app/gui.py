import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from api import OpenTDBAPI
from database import Database
import html

# Author: Niket Basu

class QuizApp(ThemedTk):
    def __init__(self):
        super().__init__(theme="arc")
        self.title("Quiz App")
        self.geometry("800x600")

        self.db = Database()
        self.api = OpenTDBAPI()
        self.current_user_id = None

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12, "bold"))
        self.style.configure("Header.TLabel", font=("Helvetica", 24, "bold"))

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame, MainMenuFrame, QuizConfigFrame, QuizFrame, ScoreHistoryFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def login(self, username, password):
        user_id = self.db.login_user(username, password)
        if user_id:
            self.current_user_id = user_id
            self.show_frame("MainMenuFrame")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self, username, password):
        if self.db.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.show_frame("LoginFrame")
        else:
            messagebox.showerror("Error", "Username already exists")

    def logout(self):
        self.current_user_id = None
        self.show_frame("LoginFrame")

class BaseFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

class LoginFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ttk.Label(self, text="Login", style="Header.TLabel").pack(pady=20)

        self.username_entry = ttk.Entry(self, font=("Helvetica", 12))
        self.password_entry = ttk.Entry(self, show="*", font=("Helvetica", 12))

        ttk.Label(self, text="Username:").pack()
        self.username_entry.pack(pady=5)
        ttk.Label(self, text="Password:").pack()
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="Login", command=self.login).pack(pady=20)
        ttk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterFrame")).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.login(username, password)

class RegisterFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ttk.Label(self, text="Register", style="Header.TLabel").pack(pady=20)

        self.username_entry = ttk.Entry(self, font=("Helvetica", 12))
        self.password_entry = ttk.Entry(self, show="*", font=("Helvetica", 12))

        ttk.Label(self, text="Username:").pack()
        self.username_entry.pack(pady=5)
        ttk.Label(self, text="Password:").pack()
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="Register", command=self.register).pack(pady=20)
        ttk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginFrame")).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.register(username, password)

class MainMenuFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ttk.Label(self, text="Main Menu", style="Header.TLabel").pack(pady=20)

        ttk.Button(self, text="Start Quiz", command=lambda: controller.show_frame("QuizConfigFrame")).pack(pady=10)
        ttk.Button(self, text="Score History", command=self.show_score_history).pack(pady=10)
        ttk.Button(self, text="Logout", command=controller.logout).pack(pady=10)

    def show_score_history(self):
        self.controller.frames["ScoreHistoryFrame"].load_scores()
        self.controller.show_frame("ScoreHistoryFrame")

class QuizConfigFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ttk.Label(self, text="Quiz Configuration", style="Header.TLabel").pack(pady=20)

        self.num_questions_entry = ttk.Entry(self, font=("Helvetica", 12))
        self.category_combobox = ttk.Combobox(self, font=("Helvetica", 12))
        self.difficulty_combobox = ttk.Combobox(self, values=["Any", "easy", "medium", "hard"], font=("Helvetica", 12))
        self.type_combobox = ttk.Combobox(self, values=["Any", "multiple", "boolean"], font=("Helvetica", 12))

        ttk.Label(self, text="Number of Questions:").pack()
        self.num_questions_entry.pack(pady=5)
        self.num_questions_entry.insert(0, "10")

        ttk.Label(self, text="Category:").pack()
        self.category_combobox.pack(pady=5)
        categories = self.controller.api.get_categories()
        self.category_map = {"Any": None}
        if categories:
            self.category_map.update({cat['name']: cat['id'] for cat in categories})
        self.category_combobox['values'] = list(self.category_map.keys())
        self.category_combobox.set("Any")

        ttk.Label(self, text="Difficulty:").pack()
        self.difficulty_combobox.pack(pady=5)
        self.difficulty_combobox.set("Any")

        ttk.Label(self, text="Question Type:").pack()
        self.type_combobox.pack(pady=5)
        self.type_combobox.set("Any")

        ttk.Button(self, text="Start Quiz", command=self.start_quiz).pack(pady=20)
        ttk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenuFrame")).pack()

    def start_quiz(self):
        num_questions = int(self.num_questions_entry.get())
        category_name = self.category_combobox.get()
        category_id = self.category_map.get(category_name)
        difficulty = self.difficulty_combobox.get()
        quiz_type = self.type_combobox.get()

        questions = self.controller.api.get_questions(num_questions, category_id, difficulty, quiz_type)

        if questions:
            self.controller.frames["QuizFrame"].start_new_quiz(questions)
            self.controller.show_frame("QuizFrame")
        else:
            messagebox.showerror("Error", "Could not fetch questions. Please try again.")

class QuizFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.question_label = ttk.Label(self, text="", wraplength=700, font=("Helvetica", 16))
        self.question_label.pack(pady=20)

        self.answer_buttons = []
        self.selected_answer = tk.StringVar()

    def start_new_quiz(self, questions):
        self.questions = questions
        self.current_question_index = 0
        self.score = 0
        self.display_question()

    def display_question(self):
        for btn in self.answer_buttons:
            btn.destroy()
        self.answer_buttons.clear()

        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.config(text=html.unescape(question_data['question']))

            answers = question_data['incorrect_answers'] + [question_data['correct_answer']]
            import random
            random.shuffle(answers)

            for answer in answers:
                btn = ttk.Radiobutton(self, text=html.unescape(answer), value=answer, variable=self.selected_answer)
                btn.pack(anchor='w', padx=50, pady=5)
                self.answer_buttons.append(btn)

            ttk.Button(self, text="Next", command=self.next_question).pack(pady=20)
        else:
            self.show_score_summary()

    def next_question(self):
        correct_answer = self.questions[self.current_question_index]['correct_answer']
        if self.selected_answer.get() == correct_answer:
            self.score += 1

        self.current_question_index += 1
        self.display_question()

    def show_score_summary(self):
        messagebox.showinfo("Quiz Over", f"Your score: {self.score}/{len(self.questions)}")
        question_data = self.questions[0]
        category_name = question_data.get('category', 'Any')
        difficulty = question_data.get('difficulty', 'Any')
        quiz_type = question_data.get('type', 'Any')
        self.controller.db.record_score(self.controller.current_user_id, self.score, len(self.questions), category_name, difficulty, quiz_type)
        self.controller.show_frame("MainMenuFrame")

class ScoreHistoryFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ttk.Label(self, text="Score History", style="Header.TLabel").pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("Score", "Total Questions", "Category", "Difficulty", "Type", "Timestamp"), show='headings')
        self.tree.heading("Score", text="Score")
        self.tree.heading("Total Questions", text="Total Questions")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Difficulty", text="Difficulty")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenuFrame")).pack(pady=20)

    def load_scores(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        scores = self.controller.db.get_user_scores(self.controller.current_user_id)
        if scores:
            for score in scores:
                self.tree.insert("", "end", values=score)