.import streamlit as st

def load_user_categories(username): return []
def load_user_transactions(username): return []

if "categories" not in st.session_state:
    st.session_state.categories = load_user_categories(username)
if "transactions" not in st.session_state:
    st.session_state.transactions = load_user_transactions(username)
    
# --- Example: Edit Budget Limits ---
st.header("Budget Planner")

for cat in st.session_state.categories:
    st.subheader(f"{cat['emoji']} {cat['name']}")
    # Allow user to set/edit budget limit
    new_limit = st.number_input(
        f"Set budget limit for {cat['name']} (in $)", 
        min_value=0.0, 
        value=cat.get('budget_limit', 0.0), 
        key=f"limit_{cat['id']}"
    )
    cat['budget_limit'] = new_limit  # Update in session

    # Example: Calculate category spending
    spent = sum(txn['amount'] for txn in st.session_state.transactions if txn['category'] == cat['name'])
    limit = cat['budget_limit']
    percent = spent / limit if limit else 0

    # Progress bar and alert
    if limit > 0:
        st.progress(min(percent, 1.0), text=f"${spent:.2f} / ${limit:.2f} ({percent*100:.0f}%)")
        if percent >= 1.0:
            st.error(f"Over budget for {cat['name']}!")
        elif percent >= 0.9:
            st.warning(f"Almost at budget limit for {cat['name']} ({percent*100:.0f}%)")
    else:
        st.info("No budget limit set for this category.")

# Save updated categories if needed
save_user_categories(username, st.session_state.categories)