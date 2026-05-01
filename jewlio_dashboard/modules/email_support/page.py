from __future__ import annotations

import streamlit as st


def render_email_support_page() -> None:
    st.markdown('<div class="page-title">Email Support</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">This module is separated for future inbox and support tools.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Inbox", 0)
    with c2:
        st.metric("Open Tickets", 0)
    with c3:
        st.metric("Pending Replies", 0)

    st.info("Your existing email support code can be added inside modules/email_support without affecting other modules.")
