import sqlite3
from datetime import datetime
import os

# Determine absolute path to database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "chatbot.db")

def init_db():
    """
    Initializes the SQLite database and creates the necessary tables.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Chat interaction logging table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                model TEXT NOT NULL,
                user_input TEXT NOT NULL,
                response TEXT NOT NULL,
                sentiment TEXT,
                intent TEXT
            )
        """)

        # Lead information table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                name TEXT,
                email TEXT,
                phone TEXT,
                product_interest TEXT,
                notes TEXT
            )
        """)

        # Settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print(f"DEBUG: SQLite database verified at {DB_PATH}.")
    except Exception as e:
        print(f"ERROR: Could not create database -> {e}")

def get_setting(key: str, default: str = "") -> str:
    """
    Retrieves a setting value from the settings table.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return default
    except Exception as e:
        print(f"ERROR: get_setting error -> {e}")
        return default

def set_setting(key: str, value: str):
    """
    Updates or inserts a setting value into the settings table.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()
        print(f"DEBUG: Setting updated -> {key}")
    except Exception as e:
        print(f"ERROR: set_setting error -> {e}")

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)

def log_interaction(user_input: str, response: str, model: str, sentiment: str = "Unknown", intent: str = "Unknown"):
    """
    Logs chat interaction to the SQLite database.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO chat_logs (timestamp, model, user_input, response, sentiment, intent)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (datetime.now(), model, user_input, response, sentiment, intent)
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        print(f"DEBUG: [OK] Interaction logged to SQLite. (Sentiment: {sentiment})")  
    except Exception as e:
        print(f"ERROR: [FAIL] SQLite logging failed -> {e}")

def save_lead(name=None, email=None, phone=None, product=None, notes=None):
    """
    Saves lead details to the SQLite database.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO leads (timestamp, name, email, phone, product_interest, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (datetime.now(), name, email, phone, product, notes)
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        print(f"DEBUG: New LEAD saved -> {name or email}")
    except Exception as e:
        print(f"ERROR: Failed to save lead -> {e}")