
import streamlit as st
from database_setup import login_user, register_user
from add_transaction import fetch_all_transactions, show_summary, calculate_tax, check_budget_limits, predict_next_month

# --- Streamlit Page Config ---
st.set_page_config(page_title="Fintari", page_icon="logo.png", layout="centered")

# --- Header Layout ---
col1, col2, col3 = st.columns([1, 4, 2])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.markdown("<h1 style='margin: 0;'>Fintari</h1>", unsafe_allow_html=True)
with col3:
    mode = st.selectbox(" ", ["Login", "Register"], label_visibility="collapsed")

# --- Session State Setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""

# --- Login ---
if not st.session_state.logged_in and mode == "Login":
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        success, msg = login_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error(msg)

# --- Register ---
if not st.session_state.logged_in and mode == "Register":
    st.subheader("📝 Register")
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
    transactions = fetch_all_transactions(st.session_state.username)
    st.subheader("📊 Tax & Predictions")
    estimated_tax = calculate_tax(transactions)
    st.info(f"💡 Estimated tax this month: Rp {estimated_tax:,.0f}")

    pred_income, pred_expense, pred_balance = predict_next_month(transactions)
    st.markdown("### 📉 Next Month Prediction")
    st.write(f"📥 Income: Rp {pred_income:,.0f}")
    st.write(f"📤 Expense: Rp {pred_expense:,.0f}")
    st.write(f"💰 Predicted Balance: Rp {pred_balance:,.0f}")

    st.write("---")
    show_summary(transactions)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.rerun()
