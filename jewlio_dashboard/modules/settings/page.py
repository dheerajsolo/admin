from __future__ import annotations

import streamlit as st

from config import settings


def render_settings_page() -> None:
    st.markdown('<div class="page-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Dashboard configuration and provider details.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.write("API Provider:", settings.api_provider)
    st.write("WooCommerce Site:", settings.wc_site_url)
    st.write("Cache TTL Seconds:", settings.cache_ttl_seconds)
    st.write("Low Stock Threshold:", settings.low_stock_threshold)

    if st.button("Clear Cache", use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared. Refresh the dashboard.")
