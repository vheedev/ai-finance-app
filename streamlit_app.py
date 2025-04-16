import streamlit as st
from database_setup import login_user, register_user, create_tables
from add_transaction import fetch_all_transactions, show_summary, calculate_tax, check_budget_limits, predict_next_month

# Ensure database tables are initialized
create_tables()

# --- Page Config ---
st.set_page_config(page_title="Fintari", page_icon="📈", layout="centered")

# --- Header ---
col1, col2, col3 = st.columns([1, 3, 2])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.markdown("<h1 style='margin: 0;'>Fintari</h1>", unsafe_allow_html=True)
with col3:
    mode = None
    # --- Main Login/Register/Dashboard Logic ---
if not st.session_state.get("logged_in", False):
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
    # ✅ Hide dropdown after login
    st.markdown(f"Welcome back, **{st.session_state.username}**!")
        # your logged-in dashboard (tax, predictions, etc.)


# --- Session State Setup ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- Auth Section ---
if not st.session_state.logged_in:
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
                st.success(msg)
            else:
                st.error(msg)
else:
    st.success(f"Welcome back, {st.session_state.username}!")
   # ✅ Show dashboard (tax & predictions)
    transactions = fetch_all_transactions(st.session_state.username)
    estimated_tax = calculate_tax(transactions)
    st.info(f"💡 Estimated tax this month: Rp {estimated_tax:,.0f}")

    pred_income, pred_expense, pred_balance = predict_next_month(transactions)
    st.markdown("### 📈 Next Month Prediction")
    st.subheader("📈 Next Month Prediction")
    st.write(f"🔻 Income: Rp {pred_income:,.0f}")
    st.write(f"🔺 Expense: Rp {pred_expense:,.0f}")
    st.write(f"💰 Predicted Balance: Rp {pred_balance:,.0f}")

# 🔓 Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
