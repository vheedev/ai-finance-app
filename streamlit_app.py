import streamlit as st
import pandas as pd
from datetime import datetime
from database_setup import init_db, get_transactions, insert_sample_transactions
from add_transaction import add_transaction
from export_pdf_report import generate_pdf_report
from report_and_chart import save_prediction, plot_prediction
from sklearn.linear_model import LinearRegression
import sqlite3
import hashlib

DB_NAME = "finance_app.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_id(username, password):
    hashed = hash_password(password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def register_user(username, password):
    hashed = hash_password(password)
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        user_id = cursor.lastrowid
        insert_sample_transactions(user_id)
        return user_id, "Registration successful."
    except sqlite3.IntegrityError:
        return None, "Username already exists."

def calculate_tax(transactions, tax_rate=10):
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    now = datetime.now()
    monthly_income = df[(df["type"] == "income") & (df["month"] == now.month) & (df["year"] == now.year)]["amount"].sum()
    return monthly_income * tax_rate / 100

def predict_next_month(transactions):
    df = pd.DataFrame(transactions)
    df["month"] = pd.to_datetime(df["date"]).dt.month
    income = df[df["type"] == "income"].groupby("month")["amount"].sum().reset_index()
    expense = df[df["type"] == "expense"].groupby("month")["amount"].sum().abs().reset_index()
    data = pd.merge(income, expense, on="month", how="outer", suffixes=("_income", "_expense")).fillna(0)
    model_i = LinearRegression().fit(data[["month"]], data["amount_income"])
    model_e = LinearRegression().fit(data[["month"]], data["amount_expense"])
    next_month = pd.DataFrame([[datetime.now().month + 1]], columns=["month"])
    pred_income = model_i.predict(next_month)[0]
    pred_expense = model_e.predict(next_month)[0]
    return pred_income, pred_expense, pred_income - pred_expense

# --- Streamlit UI ---
st.set_page_config(page_title="AI Finance App", layout="wide")
st.title("📊 AI Financial Automation App")

init_db()

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""

if choice == "Register":
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        user_id, msg = register_user(username, password)
        if user_id:
            st.success(msg)
        else:
            st.warning(msg)

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id = get_user_id(username, password)
        if user_id:
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.username = username
            st.rerun()

        else:
            st.warning("Incorrect username or password")

if st.session_state.logged_in:
    st.success(f"Welcome, {st.session_state.username}!")

    with st.expander("➕ Add New Transaction"):
        add_transaction(st.session_state.user_id)

    transactions = get_transactions(st.session_state.user_id)
    df = pd.DataFrame(transactions)

    st.subheader("📌 Financial Summary")
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    balance = income + expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"Rp {income:,.0f}")
    col2.metric("Total Expense", f"Rp {abs(expense):,.0f}")
    col3.metric("Balance", f"Rp {balance:,.0f}")

    st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)

    st.subheader("📄 Tax & Predictions")
    estimated_tax = calculate_tax(transactions)
    st.info(f"💡 Estimated tax this month: Rp {estimated_tax:,.0f}")

    pred_income, pred_expense, pred_balance = predict_next_month(transactions)
    st.markdown("### 🔮 Next Month Prediction")
    st.write(f"📈 Income: Rp {pred_income:,.0f}")
    st.write(f"📉 Expense: Rp {pred_expense:,.0f}")
    st.write(f"💰 Predicted Balance: Rp {pred_balance:,.0f}")

    save_prediction(pred_income, pred_expense, pred_balance)
    plot_prediction(pred_income, pred_expense, pred_balance)

    st.download_button("📥 Download PDF Report", generate_pdf_report(st.session_state.username, pred_income, pred_expense, pred_balance, estimated_tax), file_name="financial_report.pdf")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.experimental_rerun()
