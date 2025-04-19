# db_connection.py
"""
Handles establishing and closing the database connection.
Uses context managers for safer handling.
"""
import sqlite3
import config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(config.DATABASE_FILE)
        # Return rows as dictionaries for easier access by column name
        conn.row_factory = sqlite3.Row
        logging.info(f"Successfully connected to database: {config.DATABASE_FILE}")
        # Enable foreign key constraint enforcement (off by default in sqlite3)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None

# Example of using the connection directly (less safe than context manager)
# def close_db_connection(conn):
#     """Closes the database connection."""
#     if conn:
#         try:
#             conn.close()
#             logging.info("Database connection closed.")
#         except sqlite3.Error as e:
#             logging.error(f"Error closing database connection: {e}")

# We will primarily use context managers in other files for safety