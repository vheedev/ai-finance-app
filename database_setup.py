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

# Automatically create tables on import
create_tables()

