from __future__ import annotations

import streamlit as st


def render_sidebar() -> str:
    st.sidebar.markdown("<div class='sidebar-logo'>Jewlio</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='sidebar-caption'>Operations Dashboard</div>", unsafe_allow_html=True)

    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Orders", "Inventory", "Shipping", "Returns", "Reports", "Settings"],
        label_visibility="collapsed",
    )

    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.caption("Demo mode enabled until API keys are added.")

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    return page
