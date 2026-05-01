from __future__ import annotations

import pandas as pd
import streamlit as st

from services.product_service import get_normalized_products_df
from utils.formatters import money


def render_inventory_page() -> None:
    st.markdown('<div class="page-title">Inventory</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Monitor products, stock and low inventory in read-only mode.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df = get_normalized_products_df(100)

    if df.empty:
        st.info("No products found.")
        return

    stock_qty = pd.to_numeric(df["stock_quantity"], errors="coerce").fillna(0)
    low_stock = int(((stock_qty > 0) & (stock_qty <= 5)).sum())
    out_stock = int((stock_qty <= 0).sum())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Products", len(df))
    with c2:
        st.metric("Low Stock", low_stock)
    with c3:
        st.metric("Out of Stock", out_stock)
    with c4:
        st.metric("Total Stock Units", int(stock_qty.sum()))

    st.markdown("<br>", unsafe_allow_html=True)

    filter_col, search_col = st.columns([1, 2])
    with filter_col:
        status_options = ["All"] + sorted([x for x in df["status"].dropna().astype(str).unique().tolist() if x])
        selected_status = st.selectbox("Stock Status", status_options)
    with search_col:
        search_text = st.text_input("Search", placeholder="Search product name, SKU or category")

    filtered = df.copy()
    if selected_status != "All":
        filtered = filtered[filtered["status"].astype(str) == selected_status]
    if search_text:
        search = search_text.lower().strip()
        filtered = filtered[
            filtered.astype(str).apply(lambda row: row.str.lower().str.contains(search, na=False).any(), axis=1)
        ]

    cols = ["product_id", "name", "sku", "category", "price", "stock_quantity", "stock_status", "status", "total_sold"]
    table_df = filtered[cols].copy()
    table_df["price"] = table_df["price"].apply(money)

    st.dataframe(table_df, use_container_width=True, hide_index=True)

    csv = filtered[cols].to_csv(index=False).encode("utf-8")
    st.download_button("Download Inventory CSV", csv, "inventory.csv", "text/csv", use_container_width=True)
