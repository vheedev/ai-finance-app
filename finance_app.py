import os
import hashlib
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

from report_and_chart import save_prediction, plot_prediction
from export_pdf_report import generate_pdf_report
from database_setup import init_db, insert_sample_transactions, get_transactions

USERS_DB = "users.csv"
DB_NAME = "finance_app.db"

# --- User Authentication ---

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    init_db()
    hashed = hash_password(password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        user_id = cursor.lastrowid
        insert_sample_transactions(user_id)  # Insert demo data
        return True, "Registration successful."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def login_user(username, password):
    init_db()
    hashed = hash_password(password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed))
    row = cursor.fetchone()
    conn.close()
    if row:
        return True, row[0], "Login successful."
    return False, None, "Incorrect username or password."

# --- Budget Summary ---

def show_summary(transactions):
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"])
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    balance = income + expense

    print("\n==== Financial Summary ====")
    print(f"Total Income : Rp {income:,.0f}")
    print(f"Total Expense: Rp {abs(expense):,.0f}")
    print(f"Balance      : Rp {balance:,.0f}")
    print("\n==== Transactions ====")
    print(df[["date", "description", "amount", "account"]])
    print("=========================\n")

# --- Tax Calculation ---

def calculate_tax(transactions, tax_rate_percent=10):
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    current_month = datetime.today().month
    current_year = datetime.today().year

    monthly_income = df[(df["type"] == "income") & (df["month"] == current_month) & (df["year"] == current_year)]["amount"].sum()
    return monthly_income * (tax_rate_percent / 100)

# --- Budget Overspending Check ---

def check_budget_limits(transactions, personal_limit=2000000, business_limit=4000000):
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    current_month = datetime.today().month
    current_year = datetime.today().year

    df = df[(df["month"] == current_month) & (df["year"] == current_year)]

    def categorize(desc):
        desc = desc.lower()
        if "makan" in desc or "belanja" in desc:
            return "personal"
        elif "modal" in desc or "tokopedia" in desc or "bahan" in desc:
            return "business"
        else:
            return "other"

    df["category"] = df["description"].apply(categorize)

    personal_total = df[df["category"] == "personal"]["amount"].sum()
    business_total = df[df["category"] == "business"]["amount"].sum()

    alerts = []
    if abs(personal_total) > personal_limit:
        alerts.append(f"\u26a0\ufe0f Pengeluaran pribadi bulan ini melebihi batas Rp {personal_limit:,.0f}")
    if abs(business_total) > business_limit:
        alerts.append(f"\u26a0\ufe0f Pengeluaran bisnis bulan ini melebihi batas Rp {business_limit:,.0f}")

    return alerts

# --- AI Prediction of Next Month Cash Flow ---

def predict_next_month(df):
    df_summary = df.copy()
    df_summary["month"] = pd.to_datetime(df_summary["date"]).dt.month
    df_grouped = df_summary.groupby("month").agg({"amount": ["sum"]}).reset_index()
    df_grouped.columns = ["month", "total"]

    df_income = df_summary[df_summary["type"] == "income"].groupby("month")["amount"].sum().reset_index()
    df_expense = df_summary[df_summary["type"] == "expense"].groupby("month")["amount"].sum().abs().reset_index()

    df_model = pd.merge(df_income, df_expense, on="month", how="outer", suffixes=("_income", "_expense")).fillna(0)
    current_month = datetime.today().month
    X = df_model[["month"]]
    y_income = df_model["amount_income"]
    y_expense = df_model["amount_expense"]

    model_income = LinearRegression().fit(X, y_income)
    model_expense = LinearRegression().fit(X, y_expense)

    next_month = pd.DataFrame([[current_month + 1]], columns=["month"])
    predicted_income = model_income.predict(next_month)[0]
    predicted_expense = model_expense.predict(next_month)[0]
    predicted_balance = predicted_income - predicted_expense

    return predicted_income, predicted_expense, predicted_balance

# --- Main App (interactive version) ---

def main():
    print("=== Welcome to Financial AI Automation App ===")
    while True:
        choice = input("Login [1] | Register [2] | Exit [0]: ").strip()
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            success, user_id, msg = login_user(username, password)
            print(msg)
            if success:
                transactions = get_transactions(user_id)
                show_summary(transactions)
                estimated_tax = calculate_tax(transactions)
                print(f"\n\U0001F4A1 Estimated tax for this month (10%): Rp {estimated_tax:,.0f}")
                alerts = check_budget_limits(transactions)
                for alert in alerts:
                    print(alert)

                # AI Prediction Section
                income, expense, balance = predict_next_month(pd.DataFrame(transactions))
                print("\n=== Prediksi Keuangan Bulan Depan ===")
                print(f"Perkiraan Pemasukan : Rp {income:,.0f}")
                print(f"Perkiraan Pengeluaran: Rp {expense:,.0f}")
                print(f"Perkiraan Saldo      : Rp {balance:,.0f}")

                # Save prediction to Excel or CSV + show chart + export PDF
                save_prediction(income, expense, balance)
                plot_prediction(income, expense, balance)
                generate_pdf_report(username, income, expense, balance, estimated_tax)

        elif choice == "2":
            username = input("Choose Username: ")
            password = input("Choose Password: ")
            success, msg = register_user(username, password)
            print(msg)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please type 1, 2, or 0.")

# --- Entry Point ---

if __name__ == "__main__":
    main()
