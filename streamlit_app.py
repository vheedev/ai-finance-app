import streamlit as st
from database_setup import login_user, register_user
from add_transaction import fetch_all_transactions, show_summary, calculate_tax, check_budget_limits, predict_next_month
from export_pdf_report import generate_pdf_report
from report_and_chart import save_prediction, plot_prediction

# --- Streamlit Page Config ---
st.set_page_config(page_title="AI Financial Automation App", page_icon="📈", layout="centered")

# --- Logo, Title, and Dropdown (shown only if not logged in) ---
header_col1, header_col2, header_col3 = st.columns([1, 3, 2])
with header_col1:
    st.image("logo.png", width=80)
with header_col2:
    st.markdown("<h1 style='margin: 0;'>Fintari</h1>", unsafe_allow_html=True)
with header_col3:
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.selectbox("Login", ["Login", "Register"], key="mode")
    else:
        st.markdown("")  # empty cell to preserve spacing

# --- Session State Setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""

# --- Handle Login / Register Logic ---
if not st.session_state.logged_in:
    mode = st.session_state.get("mode", "Login")
    
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
                st.success("Registration successful! Please login.")
                st.session_state.mode = "Login"
                st.rerun()
            else:
                st.error(msg)

# --- Main App Interface after login ---
if st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.username}!")

    transactions = fetch_all_transactions(st.session_state.username)

    st.markdown("### 💡 Estimated Tax")
    estimated_tax = calculate_tax(transactions)
    st.info(f"💡 Estimated tax this month: Rp {estimated_tax:,.1f}")

    st.markdown("### 📊 Next Month Prediction")
    prediction = predict_next_month(transactions)
    st.write(f"🔻 Income: Rp {prediction['income']:,.0f}")
    st.write(f"🔺 Expense: Rp {prediction['expense']:,.0f}")
    st.write(f"💰 Predicted Balance: Rp {prediction['balance']:,.0f}")

    st.markdown("### 🧾 Summary Report")
    show_summary(transactions)

    st.markdown("### 🚦 Budget Alerts")
    check_budget_limits(transactions)

    st.markdown("### 📈 Prediction Chart")
    plot_prediction(prediction["income"], prediction["expense"])

    st.markdown("### 🧾 Download PDF")
    if st.button("📄 Export Report to PDF"):
        generate_pdf_report(transactions, prediction)
        st.success("Report exported!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
