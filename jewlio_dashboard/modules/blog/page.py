from __future__ import annotations

import streamlit as st

from services.blog_service import get_posts_df


def render_blog_page() -> None:
    st.markdown('<div class="page-title">Blog</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">View WordPress blog posts in read-only mode.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df = get_posts_df(50)

    if df.empty:
        st.info("No blog posts found. WordPress posts will appear here after API connection.")
        return

    st.metric("Posts", len(df))
    st.dataframe(df, use_container_width=True, hide_index=True)
