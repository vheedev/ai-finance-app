import streamlit as st
from database_setup import login_user, register_user
from add_transaction import fetch_all_transactions, calculate_tax, predict_next_month
from report_and_chart import save_prediction, plot_prediction
from export_pdf_report import generate_pdf_report

# --- Page Configuration ---
st.set_page_config(page_title="Fintari", layout="centered")

# --- Header with Logo, Title, and Dropdown ---
col1, col2, col3 = st.columns([1, 3, 2])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.markdown("<h1 style='margin: 0;'>Fintari</h1>", unsafe_allow_html=True)

# --- Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- Authentication and Main Flow ---
if not st.session_state.logged_in:
    with col3:
        mode = st.selectbox("Select Mode", ["Login", "Register"], label_visibility="collapsed")

    if mode == "Login":
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, msg = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
                st.experimental_rerun()
            else:
                st.error(msg)

    elif mode == "Register":
        st.subheader("📝 Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            success, msg = register_user(new_username, new_password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

else:
    st.success(f"Welcome back, {st.session_state.username}!")

    transactions = fetch_all_transactions(st.session_state.username)

    estimated_tax = calculate_tax(transactions)
    st.info(f"💡 Estimated tax this month: Rp {estimated_tax:,.0f}")

    pred_income, pred_expense, pred_balance = predict_next_month(transactions)
    st.markdown("### 📈 Next Month Prediction")
    st.write(f"🔻 Income: Rp {pred_income:,.0f}")
    st.write(f"🔺 Expense: Rp {pred_expense:,.0f}")
    st.write(f"💰 Predicted Balance: Rp {pred_balance:,.0f}")

    save_prediction(pred_income, pred_expense, pred_balance)
    plot_prediction(pred_income, pred_expense, pred_balance)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()