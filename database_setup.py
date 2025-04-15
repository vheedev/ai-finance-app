# database_setup.py

import pandas as pd
import os
import hashlib
import sqlite3

def create_tables():
    conn = sqlite3.connect("finance_app.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            type TEXT CHECK(type IN ('Income', 'Expense')) NOT NULL,
            username TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# --- Auth Functions ---
def login_user(username, password):
    conn = sqlite3.connect("finance_app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    conn.close()
    if user:
        return True, ""
    return False, "Invalid username or password"

def register_user(username, password):
    conn = sqlite3.connect("finance_app.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, ""
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()

# Auto-create tables when file is loaded
create_tables()
