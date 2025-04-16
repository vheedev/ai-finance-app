
import pandas as pd
import sqlite3
from datetime import datetime
from sklearn.linear_model import LinearRegression

def fetch_all_transactions(username):
    conn = sqlite3.connect("finance_app.db")
    df = pd.read_sql_query("SELECT * FROM transactions WHERE username = ?", conn, params=(username,))
    conn.close()
    return df

def show_summary(df):
    st = __import__("streamlit")
    st.dataframe(df)

def calculate_tax(df):
    income = df[df['type'] == 'Income']['amount'].sum()
    return income * 0.1

def check_budget_limits(df):
    return None  # Placeholder

def predict_next_month(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    monthly_summary = df.groupby(['month', 'type'])['amount'].sum().unstack().fillna(0)
    monthly_summary['balance'] = monthly_summary.get('Income', 0) - monthly_summary.get('Expense', 0)

    if len(monthly_summary) < 2:
        return 0, 0, 0

    X = monthly_summary.index.values.reshape(-1, 1)
    pred_income = LinearRegression().fit(X, monthly_summary['Income']).predict([[X[-1][0] + 1]])[0]
    pred_expense = LinearRegression().fit(X, monthly_summary['Expense']).predict([[X[-1][0] + 1]])[0]
    pred_balance = pred_income - pred_expense
    return pred_income, pred_expense, pred_balance
