from __future__ import annotations

import streamlit as st

from services.order_service import get_normalized_orders_df
from utils.formatters import money


def render_shipping_page() -> None:
    st.markdown('<div class="page-title">Shipping</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Monitor shipping-ready orders. Shiprocket actions can be added later.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df = get_normalized_orders_df(100)

    if df.empty:
        st.info("No shipping data found.")
        return

    shipping_df = df[df["status"].astype(str).str.contains("processing|pending|on-hold|hold", case=False, na=False)].copy()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Ready to Process", len(shipping_df))
    with c2:
        st.metric("COD Collectable", money(shipping_df["cod_due"].sum()))
    with c3:
        st.metric("Order Value", money(shipping_df["total"].sum()))

    st.markdown("<br>", unsafe_allow_html=True)

    cols = ["order_id", "date", "customer", "phone", "city", "product", "sku", "qty", "total", "cod_due", "status", "shipping_status"]
    table_df = shipping_df[cols].copy()
    table_df["total"] = table_df["total"].apply(money)
    table_df["cod_due"] = table_df["cod_due"].apply(money)

    st.dataframe(table_df, use_container_width=True, hide_index=True)
