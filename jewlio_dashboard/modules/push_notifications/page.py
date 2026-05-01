from __future__ import annotations

import streamlit as st


def render_push_notifications_page() -> None:
    st.markdown('<div class="page-title">Push Notifications</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">This module is separated for future campaigns, tokens and scheduled notifications.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Subscribers", 0)
    with c2:
        st.metric("Campaigns", 0)
    with c3:
        st.metric("Scheduled", 0)

    st.info("Push notification logic can be added inside modules/push_notifications and adapters/push_adapter.")
