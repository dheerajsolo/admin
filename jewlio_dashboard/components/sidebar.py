from __future__ import annotations

import streamlit as st
from textwrap import dedent


SECTIONS = {
    "Overview": ["Overview"],
    "Commerce": ["Orders", "Inventory", "Shipping"],
    "Content": ["Blog", "Email Support", "Push Notifications"],
    "Analytics": ["Reports"],
    "System": ["Settings"],
}


def html(content: str) -> None:
    st.sidebar.markdown(dedent(content), unsafe_allow_html=True)


def render_sidebar() -> str:
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Overview"

    html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-title">Jewlio</div>
            <div class="sidebar-subtitle">Dashboard</div>
        </div>
        """
    )

    for section, pages in SECTIONS.items():
        html(f'<div class="sidebar-section">{section}</div>')
        for page in pages:
            if st.sidebar.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.selected_page = page
                st.rerun()

    html('<div class="sidebar-footer"></div>')

    if st.sidebar.button("Logout", key="logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.selected_page = "Overview"
        st.rerun()

    return st.session_state.selected_page
