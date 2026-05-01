from __future__ import annotations

from textwrap import dedent

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from services.order_service import get_normalized_orders_df
from services.product_service import get_normalized_products_df


def html(content: str) -> None:
    st.markdown(dedent(content), unsafe_allow_html=True)


def money(value) -> str:
    try:
        return f"Rs. {float(value):,.0f}"
    except Exception:
        return "Rs. 0"


def to_float(value) -> float:
    try:
        if value is None:
            return 0.0
        return float(str(value).replace(",", "").replace("Rs.", "").replace("₹", "").strip())
    except Exception:
        return 0.0


def metric_card(title: str, value: str, badge_text: str, badge_type: str = "soft", dark: bool = False) -> str:
    dark_class = "dark" if dark else ""

    return dedent(
        f"""
        <div class="metric-card {dark_class}">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <span class="metric-badge {badge_type}">{badge_text}</span>
        </div>
        """
    )


def sales_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    if not df.empty and "date" in df.columns and "total" in df.columns:
        temp = df.copy()
        temp["date"] = pd.to_datetime(temp["date"], errors="coerce")
        temp["total"] = temp["total"].apply(to_float)
        temp = temp.dropna(subset=["date"])
        temp = temp.sort_values("date")

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
        height=360,
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

    if not products_df.empty and "category" in products_df.columns:
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
                    marker=dict(
                        colors=["#02224F", "#25343F", "#BFC9D1", "#8EA1B2", "#D9E0E5"]
                    ),
                )
            )

    fig.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(font=dict(size=11, color="#25343F")),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#25343F"),
    )

    return fig


def recent_orders_table(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No orders found.")
        return

    required_cols = [
        "order_id",
        "date",
        "customer",
        "phone",
        "city",
        "product",
        "sku",
        "qty",
        "total",
        "status",
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    table_df = df[required_cols].copy().head(8)
    table_df["total"] = table_df["total"].apply(money)

    st.dataframe(table_df, use_container_width=True, hide_index=True)


def render_overview_page() -> None:
    orders_df = get_normalized_orders_df(80)
    products_df = get_normalized_products_df(100)

    left_head, right_head = st.columns([4, 1.3])

    with left_head:
        html(
            """
            <div>
                <div class="page-title">Overview</div>
                <div class="page-subtitle">Business snapshot from your store data.</div>
            </div>
            """
        )

    with right_head:
        html('<div class="search-box">Search anything</div>')

    st.markdown("<br>", unsafe_allow_html=True)

    total_sales = orders_df["total"].sum() if not orders_df.empty else 0
    total_orders = len(orders_df)

    if not orders_df.empty:
        pending_shipments = orders_df["status"].astype(str).str.lower().isin(
            ["processing", "pending", "on-hold", "pending payment"]
        ).sum()
    else:
        pending_shipments = 0

    if not products_df.empty:
        low_stock = (pd.to_numeric(products_df["stock_quantity"], errors="coerce").fillna(0) <= 5).sum()
    else:
        low_stock = 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        html(metric_card("Total Revenue", money(total_sales), "Store revenue", "success", True))

    with c2:
        html(metric_card("Total Orders", f"{total_orders:,}", "Recent orders", "soft"))

    with c3:
        html(metric_card("Pending Shipping", f"{pending_shipments:,}", "Needs attention", "warn"))

    with c4:
        html(metric_card("Low Stock", f"{low_stock:,}", "Check inventory", "soft"))

    st.markdown("<br>", unsafe_allow_html=True)

    main_col, side_col = st.columns([2.2, 1])

    with main_col:
        html(
            """
            <div class="panel-card chart-head">
                <div class="panel-title">Revenue Overview</div>
                <div class="panel-subtitle">Revenue trend from recent orders.</div>
            </div>
            """
        )

        st.plotly_chart(sales_chart(orders_df), use_container_width=True)

    with side_col:
        html(
            """
            <div class="panel-card chart-head">
                <div class="panel-title">Top Categories</div>
                <div class="panel-subtitle">Product category distribution.</div>
            </div>
            """
        )

        st.plotly_chart(category_chart(products_df), use_container_width=True)

        with st.container(border=True):
            st.markdown("### Monthly Goals")
            st.caption("Track progress toward targets.")

            st.markdown("**Revenue**")
            st.progress(78)
            st.caption("Current progress: 78%")

            st.markdown("**Orders**")
            st.progress(64)
            st.caption("Current progress: 64%")

            st.markdown("**Inventory Health**")
            st.progress(86)
            st.caption("Current progress: 86%")

    st.markdown("<br>", unsafe_allow_html=True)

    html(
        """
        <div class="table-card">
            <div class="table-title">Recent Orders</div>
            <div class="table-subtitle">Latest transactions from your store.</div>
        </div>
        """
    )

    recent_orders_table(orders_df)
