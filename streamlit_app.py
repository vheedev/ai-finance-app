import streamlit as st
from auth import login, register

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.image("logo.png", width=100)
st.title("Sign In to Fintari")

if "username" not in st.session_state:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        user = st.text_input("Username", key="login_user")
        pwd = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Login"):
            ok, msg = login(user, pwd)
            if ok:
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

st.success(f"Hello, {st.session_state['username']}! Use the sidebar to navigate.")