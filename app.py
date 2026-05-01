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
        st.markdown(
            f"<style>{css_file.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def money(value):
    try:
        return f"₹{float(value):,.0f}"
    except Exception:
        return "₹0"


def to_float(value):
    try:
        if value is None:
            return 0.0
        return float(str(value).replace(",", "").replace("₹", "").strip())
    except Exception:
        return 0.0


def find_col(df, possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def normalize_orders(raw_orders):
    df = pd.DataFrame(raw_orders)

    if df.empty:
        return pd.DataFrame()

    order_col = find_col(df, ["order_id", "id", "Order ID", "Order"])
    date_col = find_col(df, ["date", "date_created", "order_date", "Date"])
    total_col = find_col(df, ["total", "order_total", "amount", "total_amount", "Total", "Amount"])
    status_col = find_col(df, ["status", "order_status", "Status"])
    customer_col = find_col(df, ["customer", "customer_name", "name", "Customer"])
    phone_col = find_col(df, ["phone", "billing_phone", "Phone"])
    city_col = find_col(df, ["city", "billing_city", "City"])
    product_col = find_col(df, ["product", "products", "Product"])
    sku_col = find_col(df, ["sku", "SKU"])
    qty_col = find_col(df, ["qty", "quantity", "Qty"])

    clean = pd.DataFrame()

    clean["order_id"] = df[order_col] if order_col else ""
    clean["date"] = df[date_col] if date_col else ""
    clean["total"] = df[total_col].apply(to_float) if total_col else 0
    clean["status"] = df[status_col] if status_col else ""
    clean["customer"] = df[customer_col] if customer_col else ""
    clean["phone"] = df[phone_col] if phone_col else ""
    clean["city"] = df[city_col] if city_col else ""
    clean["product"] = df[product_col] if product_col else ""
    clean["sku"] = df[sku_col] if sku_col else ""
    clean["qty"] = df[qty_col] if qty_col else ""

    return clean


def normalize_products(raw_products):
    df = pd.DataFrame(raw_products)

    if df.empty:
        return pd.DataFrame()

    name_col = find_col(df, ["name", "product_name", "Product", "Name"])
    sku_col = find_col(df, ["sku", "SKU"])
    stock_col = find_col(df, ["stock_quantity", "stock", "Stock", "qty"])
    category_col = find_col(df, ["category", "categories", "Category"])
    price_col = find_col(df, ["price", "regular_price", "sale_price", "Price"])

    clean = pd.DataFrame()

    clean["name"] = df[name_col] if name_col else ""
    clean["sku"] = df[sku_col] if sku_col else ""
    clean["stock_quantity"] = df[stock_col].apply(to_float) if stock_col else 0
    clean["category"] = df[category_col] if category_col else "Uncategorized"
    clean["price"] = df[price_col].apply(to_float) if price_col else 0

    return clean


def metric_card(title, value, badge_text, badge_type="soft", dark=False):
    dark_class = "dark" if dark else ""
    return f"""
    <div class="metric-card {dark_class}">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <span class="metric-badge {badge_type}">{badge_text}</span>
    </div>
    """


def sales_chart(df):
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
    )
    fig.update_xaxes(showgrid=False, color="#5E6B75")
    fig.update_yaxes(showgrid=True, gridcolor="#E1E7EB", color="#5E6B75")

    return fig


def category_chart(products_df):
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
                    hole=0.65,
                    textinfo="none",
                    marker=dict(
                        colors=["#02224F", "#25343F", "#BFC9D1", "#8EA1B2", "#D9E0E5"]
                    ),
                )
            )

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(font=dict(size=11)),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return fig


def recent_orders_table(df):
    if df.empty:
        st.info("No orders found.")
        return

    table_df = df[["order_id", "date", "customer", "phone", "city", "product", "sku", "qty", "total", "status"]].copy()
    table_df = table_df.head(8)

    table_df["total"] = table_df["total"].apply(money)

    st.dataframe(table_df, use_container_width=True, hide_index=True)


load_css()
render_sidebar("Dashboard")

orders_raw = get_orders()
products_raw = get_products()

orders_df = normalize_orders(orders_raw)
products_df = normalize_products(products_raw)

left_head, right_head = st.columns([4, 1.3])

with left_head:
    st.markdown(
        """
        <div>
            <div class="page-title">Dashboard</div>
            <div class="page-subtitle">Welcome back. Here's what's happening with your business today.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_head:
    st.markdown(
        '<div class="search-box">Search anything...</div>',
        unsafe_allow_html=True,
    )

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
    low_stock = (products_df["stock_quantity"] <= 5).sum()
else:
    low_stock = 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(metric_card("Total Revenue", money(total_sales), "+ good growth", "success", True), unsafe_allow_html=True)

with c2:
    st.markdown(metric_card("Total Orders", f"{total_orders:,}", "live orders", "soft"), unsafe_allow_html=True)

with c3:
    st.markdown(metric_card("Pending Shipments", f"{pending_shipments:,}", "needs attention", "warn"), unsafe_allow_html=True)

with c4:
    st.markdown(metric_card("Low Stock", f"{low_stock:,}", "check inventory", "soft"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

main_col, side_col = st.columns([2.2, 1])

with main_col:
    st.markdown(
        """
        <div class="panel-card">
            <div class="panel-title">Overview</div>
            <div class="panel-subtitle">Revenue trend from your recent orders</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(sales_chart(orders_df), use_container_width=True)

with side_col:
    st.markdown(
        """
        <div class="panel-card">
            <div class="panel-title">Top Categories</div>
            <div class="panel-subtitle">Where your products are concentrated</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(category_chart(products_df), use_container_width=True)

    st.markdown(
        """
        <div class="panel-card" style="margin-top:16px;">
            <div class="panel-title">Monthly Goals</div>
            <div class="panel-subtitle">Track progress toward targets</div>

            <div class="goal-row">
                <div class="goal-label">Revenue</div>
                <div class="progress-wrap">
                    <div class="progress-fill" style="width:78%;"></div>
                </div>
                <div class="goal-meta">Current progress: 78%</div>
            </div>

            <div class="goal-row">
                <div class="goal-label">Orders</div>
                <div class="progress-wrap">
                    <div class="progress-fill" style="width:64%; background:#25343F;"></div>
                </div>
                <div class="goal-meta">Current progress: 64%</div>
            </div>

            <div class="goal-row">
                <div class="goal-label">Inventory Health</div>
                <div class="progress-wrap">
                    <div class="progress-fill" style="width:86%; background:#BFC9D1;"></div>
                </div>
                <div class="goal-meta">Current progress: 86%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

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
