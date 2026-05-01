
from __future__ import annotations

import pandas as pd
import streamlit as st

from services.order_service import get_normalized_orders_df


def money(value) -> str:
    try:
        return f"Rs. {float(value):,.0f}"
    except Exception:
        return "Rs. 0"


def render_orders_page() -> None:
    st.markdown('<div class="page-title">Orders</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">View and monitor store orders in read-only mode.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    orders_df = get_normalized_orders_df(100)

    if orders_df.empty:
        st.info("No orders found.")
        return

    filter_col_1, filter_col_2, filter_col_3 = st.columns([1.2, 1.2, 2])

    with filter_col_1:
        status_options = ["All"] + sorted(
            [x for x in orders_df["status"].dropna().astype(str).unique().tolist() if x]
        )
        selected_status = st.selectbox("Status", status_options)

    with filter_col_2:
        payment_options = ["All"] + sorted(
            [x for x in orders_df["payment_method"].dropna().astype(str).unique().tolist() if x]
        )
        selected_payment = st.selectbox("Payment", payment_options)

    with filter_col_3:
        search_text = st.text_input("Search", placeholder="Search order, customer, phone, city or product")

    filtered = orders_df.copy()

    if selected_status != "All":
        filtered = filtered[filtered["status"].astype(str) == selected_status]

    if selected_payment != "All":
        filtered = filtered[filtered["payment_method"].astype(str) == selected_payment]

    if search_text:
        search = search_text.lower().strip()
        filtered = filtered[
            filtered.astype(str).apply(
                lambda row: row.str.lower().str.contains(search, na=False).any(),
                axis=1,
            )
        ]

    summary_col_1, summary_col_2, summary_col_3, summary_col_4 = st.columns(4)

    with summary_col_1:
        st.metric("Orders", len(filtered))

    with summary_col_2:
        st.metric("Revenue", money(filtered["total"].sum()))

    with summary_col_3:
        st.metric("COD Due", money(filtered["cod_due"].sum()))

    with summary_col_4:
        pending_count = filtered["status"].astype(str).str.contains(
            "processing|pending|on-hold|hold",
            case=False,
            na=False,
        ).sum()
        st.metric("Pending", int(pending_count))

    st.markdown("<br>", unsafe_allow_html=True)

    display_columns = [
        "order_id",
        "date",
        "customer",
        "phone",
        "city",
        "product",
        "sku",
        "qty",
        "payment_method",
        "total",
        "paid_amount",
        "cod_due",
        "status",
    ]

    for col in display_columns:
        if col not in filtered.columns:
            filtered[col] = ""

    table_df = filtered[display_columns].copy()
    table_df["total"] = table_df["total"].apply(money)
    table_df["paid_amount"] = table_df["paid_amount"].apply(money)
    table_df["cod_due"] = table_df["cod_due"].apply(money)

    st.dataframe(table_df, use_container_width=True, hide_index=True)

    csv_df = filtered[display_columns].copy()
    csv = csv_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Orders CSV",
        data=csv,
        file_name="orders.csv",
        mime="text/csv",
        use_container_width=True,
    )
