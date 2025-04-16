import streamlit as st
from database_setup      import login_user, register_user
from add_transaction     import (
    fetch_all_transactions,
    show_summary,
    calculate_tax,
    check_budget_limits,
    predict_next_month,
)
from export_pdf_report   import generate_pdf_report
from report_and_chart    import plot_prediction

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

    # fetch data + predictions
    txns = fetch_all_transactions(st.session_state.username)
    inc, exp, bal = predict_next_month(txns)

    # build your dict exactly once
    prediction = {
        "income":  inc,
        "expense": exp,
        "balance": bal,
    }

    # DEBUG: see exactly what prediction contains
    st.write("DEBUG:", prediction)

    # STOP the script right here—nothing below will run
    st.stop()

    # --- PDF button top‑right of content ---
    c1, c2 = st.columns([7, 3])
    with c2:
        if st.button("📄 Export Report to PDF", key="export_pdf"):
            generate_pdf_report(txns, prediction)
            st.success("Report exported!")

    # --- Chart ---
    st.markdown("### 📈 Prediction Chart")
    plot_prediction(inc, exp, bal)

    # --- Numbers ---
    st.markdown("DEBUG: prediction dict is → 📊 Next Month Prediction")
    st.write(f"🔻 Income: Rp {prediction['income']:,.0f}")
    st.write(f"🔺 Expense: Rp {prediction['expense']:,.0f}")
    st.write(f"💰 Predicted Balance: Rp {prediction['balance']:,.0f}")

    # --- Rest of dashboard ---
    st.markdown("### 🧾 Summary Report")
    show_summary(txns)

    st.markdown("### 💡 Estimated Tax")
    est_tax = calculate_tax(txns)
    st.info(f"💡 Estimated tax this month: Rp {est_tax:,.1f}")

    st.markdown("### 🚦 Budget Alerts")
    check_budget_limits(txns)
