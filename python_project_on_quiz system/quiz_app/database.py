
import sqlite3
import bcrypt
import os

# Author: Niket Basu

# Get the absolute path to the directory where this script is located
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path for the database file inside the app directory
_DB_PATH = os.path.join(_APP_DIR, "quiz_app.db")


class Database:
    def __init__(self, db_name=_DB_PATH):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates the necessary tables if they don't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                category TEXT,
                difficulty TEXT,
                quiz_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        self.conn.commit()

    def register_user(self, username, password):
        """Registers a new user with a hashed password."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def login_user(self, username, password):
        """Logs in a user by verifying their password."""
        self.cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user_data = self.cursor.fetchone()
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1]):
            return user_data[0]  # Return user_id
        return None

    def record_score(self, user_id, score, total_questions, category, difficulty, quiz_type):
        """Records a user's quiz score."""
        self.cursor.execute("""
            INSERT INTO scores (user_id, score, total_questions, category, difficulty, quiz_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, score, total_questions, category, difficulty, quiz_type))
        self.conn.commit()

    def get_user_scores(self, user_id):
        """Retrieves all scores for a specific user."""
        self.cursor.execute("""
            SELECT score, total_questions, category, difficulty, quiz_type, timestamp
            FROM scores
            WHERE user_id = ?
            ORDER BY timestamp DESC
        """, (user_id,))
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()

