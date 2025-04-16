import pandas as pd
import sqlite3
from datetime import datetime
from sklearn.linear_model import LinearRegression

def fetch_all_transactions(username):
    conn = sqlite3.connect("finance_app.db")
    df = pd.read_sql_query("SELECT * FROM transactions WHERE username = ?", conn, params=(username,))
    conn.close()
    return df

def calculate_tax(df):
    income = df[df["type"] == "Income"]["amount"].sum()
    return round(income * 0.10, 2)

def check_budget_limits(df):
    alerts = []
    category_sum = df[df["type"] == "Expense"].groupby("description")["amount"].sum()
    for category, amount in category_sum.items():
        if abs(amount) > 3000000:
            alerts.append((category, amount))
    return alerts

def predict_next_month(df):
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["amount"] = df["amount"].astype(float)
    
    df["income"] = df["amount"].where(df["type"] == "Income", 0)
    df["expense"] = df["amount"].where(df["type"] == "Expense", 0).abs()
    
    monthly = df.groupby(["year", "month"]).sum(numeric_only=True).reset_index()
    if len(monthly) < 2:
        return 0, 0, 0

    monthly["index"] = range(len(monthly))
    model_income = LinearRegression().fit(monthly[["index"]], monthly["income"])
    model_expense = LinearRegression().fit(monthly[["index"]], monthly["expense"])

    next_index = len(monthly)
    pred_income = model_income.predict([[next_index]])[0]
    pred_expense = model_expense.predict([[next_index]])[0]
    pred_balance = pred_income - pred_expense
    return pred_income, pred_expense, pred_balance

def show_summary(df):
    return df.describe()