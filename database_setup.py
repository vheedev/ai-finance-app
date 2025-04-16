
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect("finance_app.db")
    cursor = conn.cursor()
    hashed = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True, "Registration successful"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("finance_app.db")
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
    user = cursor.fetchone()
    conn.close()
    if user:
        return True, "Login successful"
    return False, "Invalid username or password"

def create_tables():
    conn = sqlite3.connect("finance_app.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        type TEXT CHECK(type IN ('Income', 'Expense')) NOT NULL,
        account TEXT,
        username TEXT NOT NULL
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        type TEXT CHECK(type IN ('Income', 'Expense')) NOT NULL,
        account TEXT,
        username TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_tables()
