from __future__ import annotations

import streamlit as st

from config import settings


def is_logged_in() -> bool:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    return bool(st.session_state.logged_in)


def render_login() -> bool:
    if is_logged_in():
        return True

    st.markdown("<div class='login-shell'>", unsafe_allow_html=True)
    st.markdown("<div class='login-title'>Jewlio Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-subtitle'>Sign in to continue.</div>", unsafe_allow_html=True)

    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if password == settings.app_password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect password")

    st.markdown("</div>", unsafe_allow_html=True)
    return False
