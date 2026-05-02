
from __future__ import annotations

import streamlit as st


def render_reviews_page() -> None:
    st.markdown('<div class="page-title">Reviews</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Monitor product reviews, ratings and pending reviews.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Reviews", 0)

    with c2:
        st.metric("Pending Reviews", 0)

    with c3:
        st.metric("Average Rating", "0.0")

    st.info("Review data will be connected through WooCommerce reviews API in the next step.")
