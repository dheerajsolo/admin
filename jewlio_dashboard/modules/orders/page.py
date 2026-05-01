from __future__ import annotations

import pandas as pd
import streamlit as st

from services.order_service import get_normalized_orders_df
from utils.formatters import money


def render_orders_page() -> None:
    st.markdown('<div class="page-title">Orders</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">View and monitor store orders in read-only mode.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    orders_df = get_normalized_orders_df(100)

    if orders_df.empty:
        st.info("No orders found.")
        return

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        statuses = ["All"] + sorted([x for x in orders_df["status"].dropna().astype(str).unique().tolist() if x])
        selected_status = st.selectbox("Status", statuses)
    with c2:
        payments = ["All"] + sorted([x for x in orders_df["payment_method"].dropna().astype(str).unique().tolist() if x])
        selected_payment = st.selectbox("Payment", payments)
    with c3:
        search_text = st.text_input("Search", placeholder="Search order, customer, phone, city or product")

    filtered = orders_df.copy()
    if selected_status != "All":
        filtered = filtered[filtered["status"].astype(str) == selected_status]
    if selected_payment != "All":
        filtered = filtered[filtered["payment_method"].astype(str) == selected_payment]
    if search_text:
        search = search_text.lower().strip()
        filtered = filtered[
            filtered.astype(str).apply(lambda row: row.str.lower().str.contains(search, na=False).any(), axis=1)
        ]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Orders", len(filtered))
    with m2:
        st.metric("Revenue", money(filtered["total"].sum()))
    with m3:
        st.metric("COD Due", money(filtered["cod_due"].sum()))
    with m4:
        pending = filtered["status"].astype(str).str.contains("processing|pending|on-hold|hold", case=False, na=False).sum()
        st.metric("Pending", int(pending))

    st.markdown("<br>", unsafe_allow_html=True)

    display_columns = [
        "order_id", "date", "customer", "phone", "city", "product", "sku", "qty",
        "payment_method", "total", "paid_amount", "cod_due", "status", "shipping_status",
    ]

    table_df = filtered[display_columns].copy()
    table_df["total"] = table_df["total"].apply(money)
    table_df["paid_amount"] = table_df["paid_amount"].apply(money)
    table_df["cod_due"] = table_df["cod_due"].apply(money)

    st.dataframe(table_df, use_container_width=True, hide_index=True)

    csv = filtered[display_columns].to_csv(index=False).encode("utf-8")
    st.download_button("Download Orders CSV", csv, "orders.csv", "text/csv", use_container_width=True)
