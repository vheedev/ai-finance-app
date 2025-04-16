import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from database_setup import login_user, register_user
from add_transaction import (
    fetch_all_transactions,
    show_summary,
    calculate_tax,
    check_budget_limits,
)
from fpdf import FPDF

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
        pwd = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="login_btn"):
            success, msg = login_user(uname, pwd)
            if success:
                st.session_state.last_active = datetime.now()
                st.session_state.logged_in = True
                st.session_state.username = uname
                st.success(f"Welcome back, {uname}!")
                st.rerun()
            else:
                st.error(msg)

    else:
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
    # Session timeout: 15 min inactivity
    now = datetime.now()
    timeout = timedelta(minutes=15)
    if "last_active" not in st.session_state:
        st.session_state.last_active = now
    elif now - st.session_state.last_active > timeout:
        st.warning("Session timed out due to inactivity. Please log in again.")
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    else:
        st.session_state.last_active = now

    st.success(f"Welcome, {st.session_state.username}!")

    # Fetch transactions and ensure dates
    txns = fetch_all_transactions(st.session_state.username)
    txns['date'] = pd.to_datetime(txns['date'])

    # ——— Period selector + Download button row ———
    today = datetime.today().date()
    # last 3 closed months
    last_months = []
    first_of_month = today.replace(day=1)
    for i in range(1, 4):
        m = first_of_month - pd.DateOffset(months=i)
        last_months.append(m.strftime("%Y-%m"))
    last_months = last_months[::-1]

    # show selector and download side by side
    sel_col, btn_col = st.columns([7, 3])
    with sel_col:
        tab1, tab2 = st.tabs(["Quick Select", "Calendar View"])
        with tab1:
            sel_period = st.selectbox("Pick one of the last 3 months", last_months)
        with tab2:
            sel_date = st.date_input("Or pick any date", value=today)

        # determine year/month
        if sel_date != today:
            sel_year, sel_month = sel_date.year, sel_date.month
        else:
            sel_year, sel_month = map(int, sel_period.split("-"))

        # filter for period
        df_period = txns[
            (txns['date'].dt.year == sel_year) &
            (txns['date'].dt.month == sel_month)
        ]

    with btn_col:
        # build PDF in memory
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Financial Report", ln=1, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"User: {st.session_state.username}", ln=1)
        pdf.cell(0, 8, f"Period: {sel_year}-{sel_month:02d}", ln=1)
        pdf.ln(5)

        # summary stats
        summary = show_summary(df_period).round(2)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "Summary Statistics", ln=1)
        pdf.set_font("Arial", '', 10)
        for metric in ['count','mean','std','min','25%','50%','75%','max']:
            row = summary.loc[metric]
            pdf.cell(0, 6, f"{metric:>6}: " + ", ".join([f"{col}={val}" for col, val in row.items()]), ln=1)
        pdf.ln(5)

        # tax and alerts
        est_tax = calculate_tax(df_period)
        alerts = check_budget_limits(df_period)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, f"Estimated Tax (10%): Rp {est_tax:,.2f}", ln=1)
        pdf.ln(3)
        pdf.cell(0, 8, "Budget Alerts:", ln=1)
        pdf.set_font("Arial", '', 10)
        if not alerts:
            pdf.cell(0, 6, "None", ln=1)
        else:
            for cat, amt in alerts:
                pdf.cell(0, 6, f"- {cat}: Rp {amt:,.0f}", ln=1)

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_bytes,
            file_name=f"report_{sel_year}-{sel_month:02d}.pdf",
            mime="application/pdf",
            key="download_pdf"
        )

    # ——— Display report for period ———
    st.markdown(f"## Report for {sel_year}-{sel_month:02d}")

    st.markdown("### 📊 Summary Report")
    st.dataframe(summary)

    st.markdown("### 💡 Estimated Tax")
    st.info(f"💡 Estimated tax this month: Rp {est_tax:,.1f}")

    st.markdown("### 🚦 Budget Alerts")
    if not alerts:
        st.write("No alerts!")
    else:
        for cat, amt in alerts:
            st.write(f"- {cat}: Rp {amt:,.0f}")
