import streamlit as st
from database_setup import login_user, register_user
from add_transaction import fetch_all_transactions, show_summary, calculate_tax, check_budget_limits, predict_next_month
from export_pdf_report import generate_pdf_report
from report_and_chart import save_prediction, plot_prediction

# --- Streamlit Page Config ---
st.set_page_config(page_title="Fintari", page_icon="logo.png", layout="centered")

# --- Logo, Title, and Dropdown (shown only if not logged in) ---
header_col1, header_col2, header_col3 = st.columns([1, 4, 2])
with header_col1:
    st.image("logo.png", width=80)
with header_col2:
    st.markdown("<h1 style='text-align: center; margin: 10; padding-top: 15px;'>Fintari</h1>", unsafe_allow_html=True)
with header_col3:
    if st.session_state.get("logged_in", False):
        st.markdown("<div style='padding-top: 15px;'>", unsafe_allow_html=True)
        if st.button("📄 Export Report to PDF"):
            transactions = fetch_all_transactions(st.session_state.username)
            prediction_income, prediction_expense, prediction_balance = predict_next_month(transactions)
            
            prediction = {
                "income": prediction_income,
                "expense": prediction_expense,
                "balance": prediction_balance
            }
            
            generate_pdf_report(transactions, prediction)
            st.success("Report exported!")
    else:
        st.markdown("</div>", unsafe_allow_html=True)  # to keep spacing clean
        


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

    # --- Prediction Chart ---
    st.markdown("### 📈 Prediction Chart")
    prediction_income, prediction_expense, prediction_balance = predict_next_month(transactions)
    plot_prediction(prediction_income, prediction_expense, prediction_balance)

    st.markdown("### 📊 Next Month Prediction")
    prediction = predict_next_month(transactions)
    st.write(f"🔻 Income: Rp {prediction['income']:,.0f}")
    st.write(f"🔺 Expense: Rp {prediction['expense']:,.0f}")
    st.write(f"💰 Predicted Balance: Rp {prediction['balance']:,.0f}")

    st.markdown("### 🧾 Summary Report")
    show_summary(transactions)
    
    st.markdown("### 💡 Estimated Tax")
    estimated_tax = calculate_tax(transactions)
    st.info(f"💡 Estimated tax this month: Rp {estimated_tax:,.1f}")

    st.markdown("### 🚦 Budget Alerts")
    check_budget_limits(transactions)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
