import streamlit as st
import json
from uuid import uuid4

# Inject custom CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🗂️ Category Management")

if "categories" not in st.session_state:
    st.session_state.categories = []

def get_cat_names():
    return [cat['name'] for cat in st.session_state.categories]

def get_cat_by_name(name):
    return next((c for c in st.session_state.categories if c['name'] == name), None)

with st.expander("Add / Edit Category"):
    col1, col2 = st.columns(2)
    with col1:
        new_cat_name = st.text_input("Category Name", key="cat_name")
        parent_options = ["None"] + get_cat_names()
        parent_sel = st.selectbox("Parent Category", parent_options, key="cat_parent")
    with col2:
        new_cat_color = st.color_picker("Category Color", "#00ff00", key="cat_color")
    if st.button("Add Category", key="cat_add_btn"):
        if new_cat_name and not get_cat_by_name(new_cat_name):
            st.session_state.categories.append({
                "id": str(uuid4()),
                "name": new_cat_name,
                "color": new_cat_color,
                "parent": None if parent_sel == "None" else parent_sel
            })
            st.success(f"Added category '{new_cat_name}'!")
        else:
            st.warning("Please enter a unique category name.")

edit_cat = st.selectbox("Edit existing category", get_cat_names(), key="edit_cat_select")
if edit_cat:
    cat_obj = get_cat_by_name(edit_cat)
    col1, col2 = st.columns([2,1])
    with col1:
        edit_name = st.text_input("New Category Name", value=cat_obj['name'], key="edit_cat_name")
        edit_parent = st.selectbox("New Parent", ["None"] + [n for n in get_cat_names() if n != edit_cat], 
                                   index=(["None"] + [n for n in get_cat_names() if n != edit_cat]).index(cat_obj['parent'] if cat_obj['parent'] else "None"),
                                   key="edit_cat_parent")
    with col2:
        edit_color = st.color_picker("New Color", value=cat_obj['color'], key="edit_cat_color")
    if st.button("Save Changes", key="cat_save_btn"):
        cat_obj['name'] = edit_name
        cat_obj['color'] = edit_color
        cat_obj['parent'] = None if edit_parent == "None" else edit_parent
        st.success("Category updated!")
    if st.button("Delete Category", key="cat_del_btn"):
        st.session_state.categories = [c for c in st.session_state.categories if c['name'] != edit_cat]
        st.success(f"Category '{edit_cat}' deleted!")

# Export/Import
with st.expander("Import/Export Categories"):
    if st.button("Export Categories as JSON"):
        cat_json = json.dumps(st.session_state.categories, indent=2)
        st.download_button("Download JSON", cat_json, file_name="categories.json")
    uploaded = st.file_uploader("Import categories from JSON", type=["json"])
    if uploaded:
        try:
            cats = json.load(uploaded)
            if isinstance(cats, list) and all("name" in c for c in cats):
                st.session_state.categories = cats
                st.success("Categories imported!")
            else:
                st.error("Invalid JSON format.")
        except Exception as e:
            st.error(f"Failed to import: {e}")