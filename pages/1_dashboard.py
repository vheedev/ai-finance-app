import streamlit as st
from datetime import datetime
from add_transaction import fetch_all_transactions, show_summary, calculate_tax, check_budget_limits
from finance_insights import forecast_next_month_expense, suggest_budget, detect_recurring

# Inject custom CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Insert the welcome banner/header here
st.markdown("""
<div style='background: #e8f0fe; border-radius: 10px; padding: 20px; margin-bottom:16px;'>
    <h2 style='color:#1a237e'>AI Finance Dashboard</h2>
    <p>Welcome, <b>{}</b>! Your personalized overview.</p>
</div>
""".format(st.session_state.get("username","Guest")), unsafe_allow_html=True)


st.title("📊 Dashboard")
st.write("Your latest financial overview and smart AI insights.")

# Example: fetch all transactions for the logged-in user (replace 'demo_user' as needed)
username = st.session_state.get("username", "demo_user")
txns = fetch_all_transactions(username)
if txns.empty:
    st.warning("No data found. Please add transactions!")

summary = show_summary(txns)
st.subheader("Summary")
st.dataframe(summary)

est_tax = calculate_tax(txns)
st.info(f"Estimated Tax: Rp {est_tax:,.2f}")

alerts  = check_budget_limits(txns)
if not alerts:
    st.success("No budget alerts!")
else:
    for cat, amt in alerts:
        st.warning(f"Budget alert for {cat}: Rp {amt:,.0f}")

st.subheader("AI Insights")
forecast, f_msg = forecast_next_month_expense(txns)
st.info(f"Next Month Expense Forecast: Rp {forecast:,.0f} - {f_msg}")

budget, b_msg = suggest_budget(txns)
st.info(f"Suggested Monthly Budget: Rp {budget:,.0f} - {b_msg}")

recurring = detect_recurring(txns)
st.write("Recurring Transaction Candidates:")
if recurring is None or recurring.empty:
    st.write("No recurring transactions detected.")
else:
    st.dataframe(recurring)