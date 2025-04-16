
import streamlit as st
from database_setup import login_user, register_user
from add_transaction import fetch_all_transactions, show_summary, calculate_tax, check_budget_limits, predict_next_month
from export_pdf_report import generate_pdf_report
from report_and_chart import save_prediction, plot_prediction

# Page config
st.set_page_config(page_title="Fintari", page_icon="📈", layout="centered")

# Header layout
col1, col2, col3 = st.columns([1, 3, 2])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.markdown("<h1 style='margin: 0;'>Fintari</h1>", unsafe_allow_html=True)
with col3:
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.session_state.mode = st.selectbox("Login", ["Login", "Register"])

# Session defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""

# AUTH FLOW
if not st.session_state.logged_in:
    if st.session_state.mode == "Login":
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

    elif st.session_state.mode == "Register":
        st.subheader("📝 Register")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            success, msg = register_user(new_user, new_pass)
            if success:
                st.success(msg)
            else:
                st.error(msg)

else:
    st.success(f"Welcome back, {st.session_state.username}!")
    transactions = fetch_all_transactions(st.session_state.username)
    show_summary(transactions)

    st.subheader("💡 Estimated Tax")
    estimated_tax = calculate_tax(transactions)
    st.info(f"💡 Estimated tax this month: Rp {estimated_tax:,}")

    pred_income, pred_expense, pred_balance = predict_next_month(transactions)
    st.markdown("### 📈 Next Month Prediction")
    st.write(f"🔻 Income: Rp {pred_income:,}")
    st.write(f"🔺 Expense: Rp {pred_expense:,}")
    st.write(f"💰 Predicted Balance: Rp {pred_balance:,}")

    save_prediction(pred_income, pred_expense, pred_balance)
    plot_prediction(pred_income, pred_expense, pred_balance)

    st.download_button("📄 Download PDF Report", generate_pdf_report(
        st.session_state.username, pred_income, pred_expense, pred_balance, estimated_tax
    ), file_name="report.pdf")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
