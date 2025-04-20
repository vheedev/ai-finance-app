import streamlit as st
from datetime import date
from add_transaction import add_transaction, fetch_all_transactions

st.title("💸 Transactions")

username = st.session_state.get("username", "demo_user")
txns = fetch_all_transactions(username)
st.dataframe(txns)

st.subheader("Add Transaction")
with st.form("add_txn_form", clear_on_submit=True):
    t_date = st.date_input("Date", value=date.today())
    t_desc = st.text_input("Description")
    cat_choices = [cat["name"] for cat in st.session_state.get("categories",[])]
    t_cat = st.selectbox("Category", cat_choices)
    t_amt = st.number_input("Amount", min_value=0.0, step=0.01)
    submit = st.form_submit_button("Add Transaction")
    if submit:
        add_transaction(username, t_date, t_cat, t_amt, t_desc)
        st.success("Transaction added!")
        st.experimental_rerun()