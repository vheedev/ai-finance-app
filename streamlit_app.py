import streamlit as st
from database_setup import login_user, register_user
from add_transaction import fetch_all_transactions, show_summary, calculate_tax, check_budget_limits, predict_next_month
from export_pdf_report import generate_pdf_report
from report_and_chart import save_prediction, plot_prediction

# --- Streamlit Page Config ---
st.set_page_config(page_title="AI Financial Automation App", page_icon="logo.png", layout="centered")

# --- Logo and Header ---
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.markdown("""
        <div style='display: flex; align-items: center; justify-content: center;'>
            <h1 style='margin: 0;'>Fintari</h1>
        </div>
    """, unsafe_allow_html=True)

# --- Session State Setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""

# --- Auth Section ---
if not st.session_state.logged_in:
    col1, col2 = st.columns([2, 1])
    with col2:
        mode = st.selectbox("Login", ["Login", "Register"])

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
                st.rerun()
            else:
                st.error(msg)

    elif mode == "Register":
        st.subheader("📝 Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")

        if st.button("Register"):
            success, msg = register_user(new_username, new_password)
            if success:
                st.success("Registration successful. Please login.")
            else:
                st.error(msg)

# --- Logged In Dashboard ---
if st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.username}!")

    # --- Full Report ---
    st.subheader("💡 Estimated Tax")
    transactions = fetch_all_transactions(st.session_state.username)
    tax = calculate_tax(transactions)
    st.info(f"💡 Estimated tax this month: Rp {tax:,.0f}")

    st.subheader("📈 Next Month Prediction")
    income, expense, balance = predict_next_month(transactions)
    st.markdown(f"🔻 **Income**: Rp {income:,.0f}")
    st.markdown(f"🔺 **Expense**: Rp {expense:,.0f}")
    st.markdown(f"💰 **Predicted Balance**: Rp {balance:,.0f}")

    st.subheader("📊 Summary")
    show_summary(transactions)
    st.subheader("📉 Budget Limits")
    check_budget_limits(transactions)

    st.subheader("📤 Export")
    if st.button("Download PDF Report"):
        generate_pdf_report(transactions)
        st.success("Report generated!")

    st.subheader("📌 Charts")
    plot_prediction(transactions)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
