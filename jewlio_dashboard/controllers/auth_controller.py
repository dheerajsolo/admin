from __future__ import annotations

import streamlit as st

from config import DEMO_USERS, ROLE_ACCESS, settings


def is_logged_in() -> bool:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    return bool(st.session_state.logged_in)


def get_current_user() -> dict:
    if "current_user" not in st.session_state:
        st.session_state.current_user = {
            "email": "",
            "name": "Guest",
            "role": "Viewer",
        }

    return st.session_state.current_user


def get_current_role() -> str:
    user = get_current_user()
    return str(user.get("role", "Viewer"))


def get_allowed_pages() -> list[str]:
    role = get_current_role()
    return ROLE_ACCESS.get(role, ["Overview"])


def can_access_page(page_name: str) -> bool:
    allowed_pages = get_allowed_pages()
    return page_name in allowed_pages


def login_with_password_only(password: str) -> bool:
    if password == settings.app_password:
        st.session_state.logged_in = True
        st.session_state.current_user = {
            "email": "admin@store.com",
            "name": "Admin User",
            "role": "Admin",
        }
        return True

    return False


def login_with_demo_user(email: str, password: str) -> bool:
    if not settings.demo_users_enabled:
        return False

    user = DEMO_USERS.get(email.strip().lower())

    if not user:
        return False

    if password != user.get("password"):
        return False

    st.session_state.logged_in = True
    st.session_state.current_user = {
        "email": email.strip().lower(),
        "name": user.get("name", "User"),
        "role": user.get("role", "Viewer"),
    }

    return True


def render_login() -> bool:
    if is_logged_in():
        return True

    st.markdown("<div class='login-shell'>", unsafe_allow_html=True)
    st.markdown(f"<div class='login-title'>{settings.app_name}</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-subtitle'>Sign in to continue.</div>", unsafe_allow_html=True)

    login_mode = st.radio(
        "Login Type",
        ["Admin Password", "Staff Login"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if login_mode == "Admin Password":
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if login_with_password_only(password):
                st.rerun()
            else:
                st.error("Incorrect password")

    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if login_with_demo_user(email, password):
                st.rerun()
            else:
                st.error("Invalid email or password")

    st.markdown("</div>", unsafe_allow_html=True)
    return False


def logout() -> None:
    st.session_state.logged_in = False
    st.session_state.current_user = {
        "email": "",
        "name": "Guest",
        "role": "Viewer",
    }
    st.session_state.selected_page = "Overview"
