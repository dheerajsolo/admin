from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from components.sidebar import render_sidebar
from services.order_service import get_orders
from services.product_service import get_products


st.set_page_config(
    page_title="Jewlio Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    css_file = Path("assets/style.css")
    if css_file.exists():
        st.markdown(f"<style>{css_file.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def money(val):
    try:
        return f"₹{float(val):,.0f}"
    except Exception:
        return "₹0"


def to_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def prepare_orders_df():
    data = get_orders()
    df = pd.DataFrame(data)

    if df.empty:
        return df

    for col in ["total", "remaining_cod", "paid_amount"]:
        if col in df.columns:
            df[col] = df[col].apply(to_float)

    return df


def prepare_products_df():
    data = get_products()
    df = pd.DataFrame(data)

    if df.empty:
        return df

    if "stock_quantity" in df.columns:
        df["stock_quantity"] = pd.to_numeric(df["stock_quantity"], errors="coerce").fillna(0)

    return df


def metric_card(title, value, badge_text, badge_type="soft", dark=False):
    dark_class = "dark" if dark else ""
    return f"""
    <div class="metric-card {dark_class}">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <span class="metric-badge {badge_type}">{badge_text}</span>
    </div>
    """


def info_header():
    left, right = st.columns([4, 2])

    with left:
        st.markdown(
            """
            <div class="top-header">
                <div>
                    <div class="page-title">Dashboard</div>
                    <div class="page-subtitle">Welcome back. Here's what's happening with your business today.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            '<div style="display:flex; justify-content:flex-end; margin-top:8px;"><div class="search-box">Search anything...</div></div>',
            unsafe_allow_html=True,
        )


def sales_chart(df):
    if df.empty or "date" not in df.columns or "total" not in df.columns:
        fig = go.Figure()
        fig.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        return fig

    temp = df.copy()
    temp["date"] = pd.to_datetime(temp["date"], errors="coerce")
    temp = temp.dropna(subset=["date"])
    temp = temp.sort_values("date")

    daily = temp.groupby(temp["date"].dt.date, as_index=False)["total"].sum()
    daily["date"] = pd.to_datetime(daily["date"])

    fig = go.Figure()
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
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        xaxis_title="",
        yaxis_title="",
    )

    fig.update_xaxes(showgrid=False, color="#5E6B75")
    fig.update_yaxes(showgrid=True, gridcolor="#E1E7EB", color="#5E6B75")

    return fig


def category_chart(products_df):
    if products_df.empty or "category" not in products_df.columns:
        fig = go.Figure()
        fig.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        return fig

    temp = products_df.copy()
    temp["category"] = temp["category"].fillna("Uncategorized")
    top = temp["category"].value_counts().head(5)

    labels = list(top.index)
    values = list(top.values)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.65,
                textinfo="none",
                marker=dict(
                    colors=["#02224F", "#25343F", "#BFC9D1", "#8EA1B2", "#D9E0E5"]
                ),
            )
        ]
    )

    fig.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(orientation="v", font=dict(size=11)),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return fig


def recent_orders_table(df):
    if df.empty:
        st.info("No orders found.")
        return

    show_cols = []
    preferred = ["order_id", "date", "customer", "phone", "city", "product", "sku", "qty", "total", "status"]
    for c in preferred:
        if c in df.columns:
            show_cols.append(c)

    table_df = df[show_cols].copy().head(8)

    if "total" in table_df.columns:
        table_df["total"] = table_df["total"].apply(money)

    st.dataframe(table_df, use_container_width=True, hide_index=True)


load_css()
render_sidebar("Dashboard")

orders_df = prepare_orders_df()
products_df = prepare_products_df()

info_header()

total_sales = orders_df["total"].sum() if not orders_df.empty and "total" in orders_df.columns else 0
total_orders = len(orders_df)
pending_shipments = len(orders_df[orders_df["status"].astype(str).str.lower().isin(["processing", "pending", "on-hold"])]) if not orders_df.empty and "status" in orders_df.columns else 0
low_stock = len(products_df[products_df["stock_quantity"] <= 5]) if not products_df.empty and "stock_quantity" in products_df.columns else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(metric_card("Total Revenue", money(total_sales), "+ good growth", "success", dark=True), unsafe_allow_html=True)
with c2:
    st.markdown(metric_card("Total Orders", f"{total_orders:,}", "live orders", "soft"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_card("Pending Shipments", f"{pending_shipments:,}", "needs attention", "warn"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_card("Low Stock", f"{low_stock:,}", "check inventory", "soft"), unsafe_allow_html=True)

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

left, right = st.columns([2.2, 1])

with left:
    st.markdown(
        """
        <div class="panel-card">
            <div class="panel-title">Overview</div>
            <div class="panel-subtitle">Revenue trend from your recent orders</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    fig = sales_chart(orders_df)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown(
        """
        <div class="panel-card">
            <div class="panel-title">Top Categories</div>
            <div class="panel-subtitle">Where your products are concentrated</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cat_fig = category_chart(products_df)
    st.plotly_chart(cat_fig, use_container_width=True)

    st.markdown(
        """
        <div class="panel-card" style="margin-top:16px;">
            <div class="panel-title">Monthly Goals</div>
            <div class="panel-subtitle">Track progress toward targets</div>

            <div class="goal-row">
                <div class="goal-label">Revenue</div>
                <div class="progress-wrap"><div class="progress-fill" style="width:78%;"></div></div>
                <div class="goal-meta">Current progress: 78%</div>
            </div>

            <div class="goal-row">
                <div class="goal-label">Orders</div>
                <div class="progress-wrap"><div class="progress-fill" style="width:64%; background:#25343F;"></div></div>
                <div class="goal-meta">Current progress: 64%</div>
            </div>

            <div class="goal-row">
                <div class="goal-label">Inventory Health</div>
                <div class="progress-wrap"><div class="progress-fill" style="width:86%; background:#BFC9D1;"></div></div>
                <div class="goal-meta">Current progress: 86%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="table-card">
        <div class="table-title">Recent Orders</div>
        <div class="table-subtitle">Latest transactions from your store</div>
    </div>
    """,
    unsafe_allow_html=True,
)

recent_orders_table(orders_df)
