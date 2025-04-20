import streamlit as st
import os
import hashlib
import json
from auth import login, register

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Login | AI Finance App", page_icon="💸")

st.image("logo.png", width=100)
st.title("💸 AI Finance App")

# --- LOGIN/REGISTER FLOW ---
if "username" not in st.session_state:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        user = st.text_input("Username", key="login_user")
        pwd = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Login"):
            ok, msg = login(user, pwd)
            if ok:
                st.session_state["username"] = user
                st.success(msg)
                st.experimental_rerun()
            else:
                st.error(msg)
    with tab2:
        new_user = st.text_input("Username", key="reg_user")
        new_pwd = st.text_input("Password", type="password", key="reg_pwd")
        if st.button("Register"):
            ok, msg = register(new_user, new_pwd)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    st.stop()

# --- LOGOUT BUTTON ---
if st.button("Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# --- WELCOME BANNER ---
st.markdown("""
<div style='background: #e8f0fe; border-radius: 10px; padding: 20px; margin-bottom:16px;'>
    <h2 style='color:#1a237e'>AI Finance Dashboard</h2>
    <p>Welcome, <b>{}</b>! Your personalized overview.</p>
</div>
""".format(st.session_state.get("username","Guest")), unsafe_allow_html=True)

st.success(f"Hello, {st.session_state['username']}! Use the sidebar to navigate the app.")