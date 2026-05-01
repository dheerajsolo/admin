from __future__ import annotations

import streamlit as st


def load_css(path: str = "assets/style.css") -> None:
    try:
        with open(path, "r", encoding="utf-8") as file:
            st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def require_login(app_password: str) -> bool:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    st.markdown("### Jewlio Admin Login")
    password = st.text_input("Dashboard Password", type="password", placeholder="Enter password")
    login = st.button("Login", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if login:
        if password == app_password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong password")
    return False
