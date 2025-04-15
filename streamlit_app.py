import streamlit as st
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from export_pdf_report import generate_pdf_report
from report_and_chart import save_prediction, plot_prediction
from database_setup import login_user, register_user
from add_transaction import fetch_all_transactions, show_summary, calculate_tax, check_budget_limits, predict_next_month

# --- Streamlit App ---

st.set_page_config(page_title="AI Finance App", layout="centered")
st.title("📊 AI Financial Automation App")

# --- Session State Init ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""

# --- Login/Register Logic ---
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, msg = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error(msg)

    with tab2:
        st.subheader("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            success, msg = register_user(new_username, new_password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

# --- Main Dashboard ---
if st.session_state.logged_in:
    st.success(f"Welcome, {st.session_state.username}!")

    transactions = fetch_all_transactions()
    df = pd.DataFrame(transactions)
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

    pred_income, pred_expense, pred_balance = predict_next_month(df)
    st.markdown("### 📅 Next Month Prediction")
    st.write(f"📈 Income: Rp {pred_income:,.0f}")
    st.write(f"📉 Expense: Rp {pred_expense:,.0f}")
    st.write(f"🧮 Predicted Balance: Rp {pred_balance:,.0f}")

    save_prediction(pred_income, pred_expense, pred_balance)
    plot_prediction(pred_income, pred_expense, pred_balance)

    st.download_button("📄 Download PDF Report",
        generate_pdf_report(st.session_state.username, pred_income, pred_expense, pred_balance, estimated_tax),
        file_name="report.pdf"
    )

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.rerun()
