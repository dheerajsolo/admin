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
    st.markdown(
        """
        <style>
        :root {
            --bg: #EEEEEE;
            --primary: #02224F;
            --muted: #BFC9D1;
            --surface: #EAEFEF;
            --sidebar: #25343F;
            --text: #25343F;
            --soft-text: #5E6B75;
            --border: #D6DEE4;
            --white: #FFFFFF;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            background: var(--bg) !important;
            color: var(--text) !important;
        }

        .block-container {
            padding-top: 42px !important;
            padding-left: 3.5rem !important;
            padding-right: 3.5rem !important;
            max-width: 1500px !important;
        }

        /* Hide default Streamlit page navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: var(--sidebar) !important;
            min-width: 250px !important;
            max-width: 250px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: var(--sidebar) !important;
            padding: 34px 24px !important;
        }

        [data-testid="stSidebar"] * {
            color: #EAEFEF !important;
        }

        [data-testid="stSidebar"] .stButton {
            margin-bottom: 6px !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            height: 42px !important;
            text-align: left !important;
            justify-content: flex-start !important;
            background: transparent !important;
            border: 0 !important;
            border-radius: 12px !important;
            color: #EAEFEF !important;
            font-weight: 700 !important;
            box-shadow: none !important;
            padding: 8px 14px !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(234, 239, 239, 0.12) !important;
            color: #FFFFFF !important;
        }

        .sidebar-brand {
            padding-bottom: 24px;
            border-bottom: 1px solid rgba(234,239,239,0.15);
            margin-bottom: 24px;
        }

        .sidebar-title {
            font-size: 28px;
            font-weight: 900;
            color: #FFFFFF !important;
            margin-bottom: 6px;
            line-height: 1.1;
        }

        .sidebar-subtitle {
            font-size: 13px;
            color: #BFC9D1 !important;
        }

        .sidebar-section {
            margin: 22px 0 10px 0;
            font-size: 11px;
            font-weight: 900;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #BFC9D1 !important;
        }

        /* Header */
        .page-title {
            color: var(--text);
            font-size: 24px;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .page-subtitle {
            color: var(--soft-text);
            font-size: 14px;
        }

        .search-box {
            background: #F7F9FA;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 13px 18px;
            color: var(--soft-text);
            font-size: 14px;
        }

        /* Metric cards */
        .metric-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 20px;
            min-height: 138px;
            box-shadow: 0 1px 3px rgba(2, 34, 79, 0.06);
        }

        .metric-card.dark {
            background: var(--primary);
            border-color: var(--primary);
        }

        .metric-label {
            color: var(--soft-text);
            font-size: 14px;
            font-weight: 800;
            margin-bottom: 18px;
        }

        .metric-card.dark .metric-label {
            color: #EAEFEF;
        }

        .metric-value {
            color: var(--text);
            font-size: 27px;
            font-weight: 900;
            margin-bottom: 18px;
        }

        .metric-card.dark .metric-value {
            color: #FFFFFF;
        }

        .metric-badge {
            display: inline-block;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            background: #E4EAEE;
            color: #25343F;
        }

        .metric-badge.success {
            background: #DCEFE4;
            color: #227A4D;
        }

        .metric-badge.warn {
            background: #F4E7C8;
            color: #9A6A00;
        }

        .panel-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(2, 34, 79, 0.06);
            margin-bottom: 0;
        }

        .panel-title {
            color: var(--text);
            font-size: 17px;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .panel-subtitle {
            color: var(--soft-text);
            font-size: 13px;
        }

        .table-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(2, 34, 79, 0.06);
        }

        .table-title {
            color: var(--text);
            font-size: 17px;
            font-weight: 900;
            margin-bottom: 4px;
        }

        .table-subtitle {
            color: var(--soft-text);
            font-size: 13px;
            margin-bottom: 12px;
        }

        .goal-row {
            margin-top: 18px;
        }

        .goal-label {
            font-size: 13px;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 8px;
        }

        .goal-meta {
            font-size: 12px;
            color: var(--soft-text);
            margin-top: 6px;
        }

        .progress-wrap {
            width: 100%;
            height: 9px;
            background: #E5EAEE;
            border-radius: 999px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: var(--primary);
            border-radius: 999px;
        }

        [data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
        }

        .chart-wrap {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-top: 0;
            border-radius: 0 0 20px 20px;
            padding: 0 12px 12px 12px;
            margin-top: -8px;
        }

        .panel-card.chart-head {
            border-radius: 20px 20px 0 0;
            border-bottom: 0;
            margin-bottom: 0;
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }

            [data-testid="stSidebar"] {
                min-width: 220px !important;
                max-width: 220px !important;
            }
        }
        .active-nav button {
    background: rgba(234, 239, 239, 0.16) !important;
    color: #FFFFFF !important;
}
        </style>
        """,
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
        return pd.DataFrame(
            columns=["order_id", "date", "total", "status", "customer", "phone", "city", "product", "sku", "qty"]
        )

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
        return pd.DataFrame(columns=["name", "sku", "stock_quantity", "category", "price"])

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
        font=dict(color="#25343F"),
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


def recent_orders_table(df):
    if df.empty:
        st.info("No orders found.")
        return

    required_cols = ["order_id", "date", "customer", "phone", "city", "product", "sku", "qty", "total", "status"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    table_df = df[required_cols].copy().head(8)
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
    st.markdown(
        metric_card("Total Revenue", money(total_sales), "+ good growth", "success", True),
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        metric_card("Total Orders", f"{total_orders:,}", "live orders", "soft"),
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        metric_card("Pending Shipments", f"{pending_shipments:,}", "needs attention", "warn"),
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        metric_card("Low Stock", f"{low_stock:,}", "check inventory", "soft"),
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

main_col, side_col = st.columns([2.2, 1])

with main_col:
    st.markdown(
        """
        <div class="panel-card chart-head">
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
        <div class="panel-card chart-head">
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
