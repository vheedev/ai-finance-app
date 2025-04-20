import streamlit as st
from datetime import date
from add_transaction import add_transaction, fetch_all_transactions

# Inject custom CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "username" not in st.session_state:
    st.warning("Please log in to see the dashboard.")
    st.stop()

# Place the Logout button right after login check
if st.button("Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

st.markdown("""
<div style='background: #e8f0fe; border-radius: 10px; padding: 20px; margin-bottom:16px;'>
    <h2 style='color:#1a237e'>AI Finance Dashboard</h2>
    <p>Welcome, <b>{}</b>! Your personalized overview.</p>
</div>
""".format(st.session_state.get("username","Guest")), unsafe_allow_html=True)

def load_user_categories(username): return []
def load_user_transactions(username): return []

if "categories" not in st.session_state:
    st.session_state.categories = load_user_categories(username)
if "transactions" not in st.session_state:
    st.session_state.transactions = load_user_transactions(username)
    
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