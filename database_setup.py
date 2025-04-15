# database_setup.py

import pandas as pd
import os
import hashlib

DB_FILE = "users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=["username", "password"])
    else:
        df = pd.read_csv(DB_FILE)

    if username in df["username"].values:
        return False, "Username already exists."

    hashed_pw = hash_password(password)
    new_user = pd.DataFrame([{"username": username, "password": hashed_pw}])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return True, "Registration successful."

def login_user(username, password):
    if not os.path.exists(DB_FILE):
        return False, "No users registered yet."

    df = pd.read_csv(DB_FILE)
    hashed_pw = hash_password(password)

    if ((df["username"] == username) & (df["password"] == hashed_pw)).any():
        return True, "Login successful."
    return False, "Invalid username or password."
