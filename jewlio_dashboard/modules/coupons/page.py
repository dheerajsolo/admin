
from __future__ import annotations

import streamlit as st


def render_coupons_page() -> None:
    st.markdown('<div class="page-title">Coupons</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Track coupon usage by order and customer. This section is read-only.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Coupons Used", 0)

    with c2:
        st.metric("Discount Amount", "Rs. 0")

    with c3:
        st.metric("Orders With Coupons", 0)

    st.info("Coupon usage table will be connected in the next step.")
