from __future__ import annotations

from textwrap import dedent

import streamlit as st

from config import settings
from controllers.auth_controller import get_allowed_pages, get_current_user, logout


SECTIONS = {
    "Overview": ["Overview"],
    "Commerce": ["Orders", "Inventory", "Shipping", "Coupons", "Reviews"],
    "Content": ["Blog", "Email Support", "SEO", "Push Notifications"],
    "Analytics": ["Reports"],
    "System": ["Users", "Settings"],
}


def html(content: str) -> None:
    st.sidebar.markdown(dedent(content), unsafe_allow_html=True)


def render_sidebar() -> str:
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Overview"

    user = get_current_user()
    allowed_pages = get_allowed_pages()

    html(
        f"""
        <div class="sidebar-brand">
            <div class="sidebar-title">{settings.brand_name}</div>
            <div class="sidebar-subtitle">Operations Dashboard</div>
        </div>
        """
    )

    html(
        f"""
        <div style="padding: 0 4px 14px 4px; margin-bottom: 10px; border-bottom: 1px solid rgba(234,239,239,0.10);">
            <div style="font-size: 13px; font-weight: 800; color: #FFFFFF;">{user.get("name", "User")}</div>
            <div style="font-size: 11px; color: #BFC9D1;">{user.get("role", "Viewer")}</div>
        </div>
        """
    )

    for section, pages in SECTIONS.items():
        visible_pages = [page for page in pages if page in allowed_pages]

        if not visible_pages:
            continue

        html(f'<div class="sidebar-section">{section}</div>')

        for page in visible_pages:
            if st.sidebar.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.selected_page = page
                st.rerun()

    html('<div class="sidebar-footer"></div>')

    if st.sidebar.button("Logout", key="logout", use_container_width=True):
        logout()
        st.rerun()

    if st.session_state.selected_page not in allowed_pages:
        st.session_state.selected_page = "Overview"

    return st.session_state.selected_page
