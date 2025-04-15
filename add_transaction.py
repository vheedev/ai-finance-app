import sqlite3
import pandas as pd
import streamlit as st

def add_transaction(date, amount, category, type_, username):
    conn = sqlite3.connect("finance_app.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (date, amount, category, type, username)
        VALUES (?, ?, ?, ?, ?)
    """, (date, amount, category, type_, username))
    conn.commit()
    conn.close()

def fetch_all_transactions(username):
    conn = sqlite3.connect("finance_app.db")
    df = pd.read_sql_query("SELECT * FROM transactions WHERE username = ?", conn, params=(username,))
    conn.close()
    return df

def show_summary(df):
    income = df[df['type'] == 'Income']['amount'].sum()
    expense = df[df['type'] == 'Expense']['amount'].sum()
    balance = income - expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"Rp {income:,.0f}")
    col2.metric("Total Expense", f"Rp {expense:,.0f}")
    col3.metric("Balance", f"Rp {balance:,.0f}")

def calculate_tax(df):
    income = df[df['type'] == 'Income']['amount'].sum()
    return income * 0.10  # 10% tax assumption

def check_budget_limits(df):
    # Optional placeholder for future budgeting alerts
    pass

def predict_next_month(df):
    income = df[df['type'] == 'Income']['amount'].sum()
    expense = df[df['type'] == 'Expense']['amount'].sum()
    predicted_income = income * 1.1  # +10% income growth
    predicted_expense = expense * 1.05  # +5% inflation
    predicted_balance = predicted_income - predicted_expense
    return predicted_income, predicted_expense, predicted_balance
