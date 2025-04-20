import streamlit as st

# --- Category Management Section ---

# Initialize categories in session state if not present
if "categories" not in st.session_state:
    # Default categories, could be loaded per-user from DB
    st.session_state.categories = ["Food", "Transport", "Shopping", "Bills"]

st.markdown("## 🗂️ Category Management")

# Display categories
st.write("**Current categories:**")
st.write(st.session_state.categories)

# Add new category
new_cat = st.text_input("Add new category", key="add_cat_input")
if st.button("Add Category", key="add_cat_btn"):
    if new_cat and new_cat not in st.session_state.categories:
        st.session_state.categories.append(new_cat)
        st.success(f"Category '{new_cat}' added!")
    elif new_cat:
        st.warning("Category already exists.")
    else:
        st.warning("Please enter a category name.")

# Rename category
cat_to_rename = st.selectbox("Select category to rename", st.session_state.categories, key="rename_cat_select")
new_name = st.text_input("New name", key="rename_cat_input")
if st.button("Rename Category", key="rename_cat_btn"):
    if new_name:
        idx = st.session_state.categories.index(cat_to_rename)
        st.session_state.categories[idx] = new_name
        st.success(f"Category '{cat_to_rename}' renamed to '{new_name}'!")
    else:
        st.warning("Please enter a new category name.")

# Remove category
cat_to_remove = st.selectbox("Select category to remove", st.session_state.categories, key="remove_cat_select")
if st.button("Remove Category", key="remove_cat_btn"):
    st.session_state.categories.remove(cat_to_remove)
    st.success(f"Category '{cat_to_remove}' removed!")

# --- Suggest category based on description ---
def suggest_category(description, categories):
    desc = description.lower()
    # Simple keyword-based rules; expand as needed
    keywords = {
        "Food": ["lunch", "dinner", "coffee", "restaurant", "snack"],
        "Transport": ["uber", "taxi", "bus", "train", "gojek"],
        "Shopping": ["mall", "shop", "buy", "clothes", "amazon"],
        "Bills": ["electric", "water", "internet", "phone", "pln"],
    }
    for cat, keys in keywords.items():
        if any(word in desc for word in keys) and cat in categories:
            return cat
    return categories[0] if categories else ""

# Example usage in the Add Transaction form:
with st.form("add_txn_form", clear_on_submit=True):
    t_date = st.date_input("Date", value=date.today())
    t_desc = st.text_input("Description")
    # Suggest category:
    suggested = suggest_category(t_desc, st.session_state.categories)
    t_cat  = st.text_input("Category", value=suggested)
    t_amt  = st.number_input("Amount", min_value=0.0, step=0.01)
    submit = st.form_submit_button("Add Transaction")
    if submit:
        # Save transaction logic here
        st.success("Transaction added!")