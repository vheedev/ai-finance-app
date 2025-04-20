import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta

from database_setup import login_user, register_user

# You need to implement these functions in this file or another: 
# fetch_all_transactions, show_summary, calculate_tax, check_budget_limits, add_transaction

def fetch_all_transactions(username):
    # Dummy: Replace with your own database/data retrieval logic
    try:
        df = pd.read_csv("transactions.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["username", "date", "category", "amount", "description"])
    return df[df["username"] == username].copy()

def add_transaction(username, t_date, t_cat, t_amt, t_desc):
    try:
        df = pd.read_csv("transactions.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["username", "date", "category", "amount", "description"])
    new_row = {
        "username": username,
        "date": pd.to_datetime(t_date),
        "category": t_cat,
        "amount": t_amt,
        "description": t_desc
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("transactions.csv", index=False)

def show_summary(df):
    # Group by category and sum
    return df.groupby("category")["amount"].sum().reset_index()

def calculate_tax(df):
    # Example: 10% tax on all positive amounts ("income")
    income = df[df["amount"] > 0]["amount"].sum()
    return income * 0.10

def check_budget_limits(df):
    # Dummy: No real limits, just show if any category exceeds 5,000,000
    alerts = []
    summary = df.groupby("category")["amount"].sum()
    for cat, amt in summary.items():
        if amt > 5_000_000:
            alerts.append((cat, amt))
    return alerts

# --- Page config ---
st.set_page_config(page_title="Fintari", page_icon="logo.png", layout="centered")

# -- Hide Streamlit deprecation banners --
hide_deprecation = """
<style>
  div[data-testid="stAlert"] > div[role="alert"] {
    display: none !important;
  }
</style>
"""
st.markdown(hide_deprecation, unsafe_allow_html=True)

# --- Persist login via Query Params ---
params = st.experimental_get_query_params()
if params.get("logged_in") == ["true"] and "username" in params:
    st.session_state.logged_in = True
    st.session_state.username  = params["username"][0]

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
        st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn"):
            st.experimental_set_query_params()
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- Login / Register ---
if not st.session_state.logged_in:
    mode = st.selectbox("Select mode", ["Login", "Register"], key="mode_select")
    if mode == "Login":
        st.subheader("🔐 Login")
        with st.form("login_form", clear_on_submit=False):
            uname = st.text_input("Username", key="login_user")
            pwd = st.text_input("Password", type="password", key="login_pass")
            submitted = st.form_submit_button("Login")
            if submitted:
                success, msg = login_user(uname, pwd)
                if success:
                    st.experimental_set_query_params(logged_in="true", username=uname)
                    st.session_state.last_active = datetime.now()
                    st.session_state.logged_in = True
                    st.session_state.username = uname
                    st.success(f"Welcome back, {uname}!")
                    st.rerun()
                else:
                    st.error(msg)
    else:
        st.subheader("📝 Register")
        with st.form("register_form", clear_on_submit=False):
            new_un = st.text_input("New Username", key="reg_user")
            new_pw = st.text_input("New Password", type="password", key="reg_pass")
            submitted = st.form_submit_button("Register")
            if submitted:
                success, msg = register_user(new_un, new_pw)
                if success:
                    st.success("Registration successful! Please log in.")
                    st.rerun()
                else:
                    st.error(msg)

# --- Main app (after login) ---
else:
    # Session timeout: 15 min
    now = datetime.now()
    timeout = timedelta(minutes=15)
    if "last_active" not in st.session_state:
        st.session_state.last_active = now
    elif now - st.session_state.last_active > timeout:
        st.warning("Session timed out. Please log in again.")
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    else:
        st.session_state.last_active = now

    st.success(f"Welcome, {st.session_state.username}!")
    # 🆕 New Transaction Form
    st.subheader("🆕 Add New Transaction")
    with st.form("add_txn", clear_on_submit=True):
        t_date = st.date_input("Date", value=date.today())
        t_cat  = st.text_input("Category")
        t_amt  = st.number_input("Amount", min_value=0.0, step=0.01)
        t_desc = st.text_input("Description")
        submit = st.form_submit_button("Add Transaction")
        if submit:
            add_transaction(
                st.session_state.username,
                t_date,
                t_cat,
                t_amt,
                t_desc,
            )
            st.success("Transaction added!")
            st.rerun()

    # Fetch all transactions
    local_txns = fetch_all_transactions(st.session_state.username)
    txns = local_txns.copy()
    txns["date"] = pd.to_datetime(txns["date"])

    # Prepare periods
    today = datetime.today().date()
    first_of_month = today.replace(day=1)
    last_months = [
        (first_of_month - pd.DateOffset(months=i)).strftime("%Y-%m")
        for i in range(3, 0, -1)
    ]

    # Tabs
    tab1, tab2 = st.tabs(["Quick Select", "Calendar View"])

    # --- Quick Select ---
    with tab1:
        sel_period = st.selectbox(
            "Pick one of the last 3 months",
            last_months,
            index=last_months.index(st.session_state.get('sel_period', last_months[-1])),
            key="sel_period"
        )
        year, month = map(int, sel_period.split("-"))
        filt1 = txns[
            (txns["date"].dt.year  == year) &
            (txns["date"].dt.month == month)
        ]
        st.write("🔍 Filtered rows (Quick-Select):", filt1.shape[0])

        summary1 = show_summary(filt1)
        est_tax1 = calculate_tax(filt1)
        alerts1  = check_budget_limits(filt1)

        st.markdown("### 📊 Summary Report")
        summary1_df = summary1.copy()
        summary1_df.columns = ["Category", "Total Amount"]
        # Bar chart with matplotlib to allow scrolling
        #chart1 = summary1_df.set_index("Category")["Total Amount"]
        #fig1, ax1 = plt.subplots()
        #ax1.bar(chart1.index, chart1.values)
        #ax1.set_xlabel("Category")
        #ax1.set_ylabel("Total Amount")
        #st.pyplot(fig1)
        st.bar_chart(summary1_df.set_index("Category")["Total Amount"])
        # Table below
        st.dataframe(summary1_df, use_container_width=True)

        st.markdown("### 💡 Estimated Tax")
        st.info(f"Rp {est_tax1:,.2f}")

        st.markdown("### 🚦 Budget Alerts")
        if not alerts1:
            st.write("No alerts 🎉")
        else:
            for cat, amt in alerts1:
                st.write(f"- {cat}: Rp {amt:,.0f}")

    # --- Calendar View ---
    with tab2:
        _, btn_col = st.columns([7, 3])
        download_slot = btn_col.empty()

        start_date, end_date = st.date_input(
            "🗓 Select report range",
            value=(today.replace(day=1), today),
            format="YYYY-MM-DD"
        )
        mask = (
            (txns["date"] >= pd.to_datetime(start_date)) &
            (txns["date"] <= pd.to_datetime(end_date))
        )
        filtered = txns.loc[mask]
        st.write("🔍 Filtered rows (Calendar-View):", filtered.shape[0])

        summary = show_summary(filtered)
        est_tax = calculate_tax(filtered)
        alerts  = check_budget_limits(filtered)

        # --- PDF Report (Optional, requires fpdf) ---
        # from fpdf import FPDF
        # pdf = FPDF()
        # ... (build report as you wish)

        st.markdown("### 📊 Summary Report")
        summary_df = summary.copy()
        summary_df.columns = ["Category", "Total Amount"]
        # matplotlib chart for scrolling
        #chart2 = summary_df.set_index("Category")["Total Amount"]
        #fig2, ax2 = plt.subplots()
        #ax2.bar(chart2.index, chart2.values)
        #ax2.set_xlabel("Category")
        #ax2.set_ylabel("Total Amount")
        #st.pyplot(fig2)
        st.bar_chart(summary1_df.set_index("Category")["Total Amount"])
        # table below
        st.dataframe(summary_df, use_container_width=True)

        st.markdown("### 💡 Estimated Tax")
        st.info(f"Rp {est_tax:,.2f}")

        st.markdown("### 🚦 Budget Alerts")
        if not alerts:
            st.write("No alerts 🎉")
        else:
            for cat, amt in alerts:
                st.write(f"- {cat}: Rp {amt:,.0f}")