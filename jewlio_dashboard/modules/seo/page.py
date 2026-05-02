
from __future__ import annotations

import streamlit as st


def render_seo_page() -> None:
    st.markdown('<div class="page-title">SEO</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">SEO tasks, blog optimization and search performance tools will be managed here.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("SEO Tasks", 0)

    with c2:
        st.metric("Pending Blogs", 0)

    with c3:
        st.metric("Optimized Pages", 0)

    st.info("SEO access and workflow are ready. Data connection can be added later.")
