from database_setup
from add_transaction
from export_pdf_report
from report_and_chart
from datetime import datetime, date
import streamlit as st
import pandas as pd
import login_user, register_user
import (
    fetch_all_transactions,
    show_summary,
    calculate_tax,
    check_budget_limits,
    predict_next_month,
)
import generate_pdf_report
import plot_prediction

# --- Page config ---
st.set_page_config(page_title="Fintari", page_icon="logo.png", layout="centered")

# --- Session state defaults ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Header: logo / title / logout ---
col1, col2, col3 = st.columns([1, 4, 2])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.markdown(
        "<h1 style='text-align: center; margin: 10; padding-top: 15px;'>Fintari</h1>",
        unsafe_allow_html=True,
    )
with col3:
    if st.session_state.logged_in:
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

# --- Login / Register ---
if not st.session_state.logged_in:
    mode = st.selectbox("Select mode", ["Login", "Register"], key="mode_select")

    if mode == "Login":
        st.subheader("🔐 Login")
        uname = st.text_input("Username", key="login_user")
        pwd   = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="login_btn"):
            success, msg = login_user(uname, pwd)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = uname
                st.success(f"Welcome back, {uname}!")
                st.rerun()
            else:
                st.error(msg)

    else:  # Register
        st.subheader("📝 Register")
        new_un = st.text_input("New Username", key="reg_user")
        new_pw = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register", key="reg_btn"):
            success, msg = register_user(new_un, new_pw)
            if success:
                st.success("Registration successful! Please log in.")
                st.rerun()
            else:
                st.error(msg)

# --- Main app (after login) ---
else:
    st.success(f"Welcome, {st.session_state.username}!")

    # fetch data + predictions (predict_next_month returns a dict)
    txns = fetch_all_transactions(st.session_state.username)

    # make sure dates are datetimes
    txns['date'] = pd.to_datetime(txns['date'])
    # —— period selector ——
    today = datetime.today().date()

    # build list of the last 3 closed months
    last_months = []
    first_of_this_month = today.replace(day=1)
    for i in range(1, 4):
        m = first_of_this_month - pd.DateOffset(months=i)
        last_months.append(m.strftime("%Y-%m"))
    last_months = last_months[::-1]

    # two‐tab chooser: quick vs. calendar
    tab1, tab2 = st.tabs(["Quick Select", "Calendar View"])
    with tab1:
        sel_period = st.selectbox("Pick one of the last 3 months", last_months)
    with tab2:
        sel_date   = st.date_input("Or pick any date", value=today)

    # decide which to use
    if sel_date != today:
        sel_year, sel_month = sel_date.year, sel_date.month
    else:
        sel_year, sel_month = map(int, sel_period.split("-"))

    # filter to only that month
    df_period = txns[
        (txns['date'].dt.year  == sel_year) &
        (txns['date'].dt.month == sel_month)
    ]
    
    prediction = predict_next_month(txns)

    # now pull the numeric values out
    income  = prediction["income"]
    expense = prediction["expense"]
    balance = prediction["balance"]

    # --- PDF button top‑right of content ---
    c1, c2 = st.columns([7, 3])
    with c2:
        if st.button("📄 Export Report to PDF", key="export_pdf"):
            tax = calculate_tax(txns)
            generate_pdf_report(
                st.session_state.username,
                income,
                expense,
                balance,
                tax
            )
            st.success("Report exported!")

    # --- Chart ---
    st.markdown("### 📈 Prediction Chart")
    plot_prediction(income, expense, balance)

    # --- Numbers ---
    st.markdown("### 📊 Next Month Prediction")
    st.write(f"🔻 Income: Rp {income:,.0f}")
    st.write(f"🔺 Expense: Rp {expense:,.0f}")
    st.write(f"💰 Predicted Balance: Rp {balance:,.0f}")

    # --- Rest of dashboard ---
    st.markdown("### 🧾 Summary Report")
    show_summary(txns)

    st.markdown("### 💡 Estimated Tax")
    est_tax = calculate_tax(txns)
    st.info(f"💡 Estimated tax this month: Rp {est_tax:,.1f}")

    st.markdown("### 🚦 Budget Alerts")
    check_budget_limits(txns)
