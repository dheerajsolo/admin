from __future__ import annotations

import streamlit as st
from textwrap import dedent


PAGES = [
    "Overview",
    "Orders",
    "Inventory",
    "Shipping",
    "Blog",
    "Email Support",
    "Push Notifications",
    "Reports",
    "Settings",
]


def html(content: str) -> None:
    st.sidebar.markdown(dedent(content), unsafe_allow_html=True)


def render_sidebar() -> str:
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Overview"

    html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-title">Jewlio</div>
            <div class="sidebar-subtitle">Operations Dashboard</div>
        </div>
        """
    )

    html('<div class="sidebar-section">Main</div>')

    for page in PAGES:
        if st.sidebar.button(page, key=f"nav_{page}", use_container_width=True):
            st.session_state.selected_page = page
            st.rerun()

    html('<div class="sidebar-section">Account</div>')

    if st.sidebar.button("Logout", key="logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.selected_page = "Overview"
        st.rerun()

    return st.session_state.selected_page
