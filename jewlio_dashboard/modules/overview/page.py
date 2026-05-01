from __future__ import annotations

from textwrap import dedent

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.cards import metric_card
from services.order_service import get_normalized_orders_df
from services.product_service import get_normalized_products_df
from utils.formatters import money, to_float


def html(content: str) -> None:
    st.markdown(dedent(content), unsafe_allow_html=True)


def revenue_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    if not df.empty:
        temp = df.copy()
        temp["date"] = pd.to_datetime(temp["date"], errors="coerce")
        temp["total"] = temp["total"].apply(to_float)
        temp = temp.dropna(subset=["date"]).sort_values("date")

        if not temp.empty:
            daily = temp.groupby(temp["date"].dt.date, as_index=False)["total"].sum()
            daily["date"] = pd.to_datetime(daily["date"])

            fig.add_trace(
                go.Scatter(
                    x=daily["date"],
                    y=daily["total"],
                    mode="lines",
                    line=dict(color="#02224F", width=3),
                    fill="tozeroy",
                    fillcolor="rgba(2,34,79,0.10)",
                    name="Revenue",
                )
            )

    fig.update_layout(
        height=410,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        xaxis_title="",
        yaxis_title="",
        font=dict(color="#25343F"),
    )
    fig.update_xaxes(showgrid=False, color="#5E6B75")
    fig.update_yaxes(showgrid=True, gridcolor="#E1E7EB", color="#5E6B75")
    return fig


def category_chart(products_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    if not products_df.empty:
        temp = products_df.copy()
        temp["category"] = temp["category"].fillna("Uncategorized")
        temp["category"] = temp["category"].astype(str).apply(lambda x: x.split(",")[0].strip())
        top = temp["category"].value_counts().head(5)

        if not top.empty:
            fig.add_trace(
                go.Pie(
                    labels=list(top.index),
                    values=list(top.values),
                    hole=0.62,
                    textinfo="none",
                    marker=dict(colors=["#02224F", "#25343F", "#BFC9D1", "#EAEFEF", "#EEEEEE"]),
                )
            )

    fig.update_layout(
        height=255,
        margin=dict(l=5, r=5, t=5, b=5),
        showlegend=True,
        legend=dict(font=dict(size=11, color="#25343F")),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#25343F"),
    )
    return fig


def render_overview_page() -> None:
    orders_df = get_normalized_orders_df(100)
    products_df = get_normalized_products_df(100)

    col_a, col_b = st.columns([3, 1])
    with col_a:
        html('<div class="page-title">Dashboard</div>')
        html('<div class="page-subtitle">Welcome back. Here is what is happening with your business today.</div>')
    with col_b:
        html('<div class="search-box">Search anything</div>')

    st.markdown("<br>", unsafe_allow_html=True)

    total_revenue = orders_df["total"].sum() if not orders_df.empty else 0
    total_orders = len(orders_df)
    pending = 0
    cod_due = 0
    if not orders_df.empty:
        pending = orders_df["status"].astype(str).str.contains("processing|pending|on-hold|hold", case=False, na=False).sum()
        cod_due = orders_df["cod_due"].sum()

    low_stock = 0
    if not products_df.empty:
        low_stock = (pd.to_numeric(products_df["stock_quantity"], errors="coerce").fillna(0) <= 5).sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        html(metric_card("Total Revenue", money(total_revenue), "Recent order revenue", "+12.5%"))
    with c2:
        html(metric_card("Total Orders", f"{total_orders:,}", "Orders fetched", "+8.2%"))
    with c3:
        html(metric_card("Pending Shipping", f"{int(pending):,}", "Needs attention", "-3.1%", warn=True))
    with c4:
        html(metric_card("Low Stock", f"{int(low_stock):,}", "Check inventory", "+24.7%"))

    st.markdown("<br>", unsafe_allow_html=True)

    main_col, side_col = st.columns([2.1, 1])

    with main_col:
        with st.container(border=True):
            html('<div class="panel-title">Overview</div>')
            html('<div class="panel-subtitle">Revenue performance from recent orders.</div>')
            st.plotly_chart(revenue_chart(orders_df), use_container_width=True)

    with side_col:
        with st.container(border=True):
            html('<div class="panel-title">Top Categories</div>')
            html('<div class="panel-subtitle">Product category distribution.</div>')
            st.plotly_chart(category_chart(products_df), use_container_width=True)

        with st.container(border=True):
            html('<div class="panel-title">Monthly Goals</div>')
            html('<div class="panel-subtitle">Track progress toward targets.</div>')
            st.markdown("**Monthly Revenue**")
            st.progress(88)
            st.caption("Current progress: 88%")
            st.markdown("**New Orders**")
            st.progress(72)
            st.caption("Current progress: 72%")
            st.markdown("**Inventory Health**")
            st.progress(81)
            st.caption("Current progress: 81%")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    with left:
        with st.container(border=True):
            html('<div class="table-title">Recent Orders</div>')
            html('<div class="table-subtitle">Latest transactions from your store.</div>')

            display_cols = ["customer", "order_id", "product", "status", "total"]
            table_df = orders_df[display_cols].head(8).copy() if not orders_df.empty else pd.DataFrame(columns=display_cols)
            if not table_df.empty:
                table_df["total"] = table_df["total"].apply(money)
            st.dataframe(table_df, use_container_width=True, hide_index=True)

    with right:
        with st.container(border=True):
            html('<div class="table-title">Recent Activity</div>')
            html('<div class="table-subtitle">Latest events from your store.</div>')
            st.write("New orders loaded")
            st.write("Inventory summary updated")
            st.write("Reports cache refreshed")
