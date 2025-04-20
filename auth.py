import streamlit as st
import hashlib
import json
import os

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = hash_password(password)
    save_users(users)
    return True, "User registered!"

def login(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found"
    if users[username] != hash_password(password):
        return False, "Wrong password"
    st.session_state["username"] = username
    return True, "Login successful"