from __future__ import annotations

import streamlit as st

from config import settings
from utils.helpers import load_css, require_login
from components.sidebar import render_sidebar
from components.cards import page_header, metric_card
from services.order_service import order_summary
from services.product_service import product_summary
from services.report_service import get_sales_series, top_categories
from services.order_service import get_orders_df
from services.product_service import get_products_df
from services.shipping_service import get_shipments_df
from utils.formatters import money, number

import plotly.express as px

st.set_page_config(
    page_title="Jewlio Admin",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_css()

if not require_login(settings.app_password):
    st.stop()

page = render_sidebar()


def dashboard_page() -> None:
    page_header("Welcome back, Dheeraj", "Here are today's stats from your store")

    orders = order_summary()
    products = product_summary()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Sales", money(orders["sales"]), "+12.5%", "good", dark=True)
    with c2:
        metric_card("Total Orders", number(orders["orders"]), "+8 orders", "good")
    with c3:
        metric_card("Pending Shipments", number(orders["pending"]), "Need action", "warn")
    with c4:
        metric_card("Low Stock", number(products["low_stock"] + products["out_stock"]), "Check inventory", "bad")

    left, right = st.columns([2.1, 1])
    with left:
        st.markdown("<div class='panel-title'>Sales Performance</div><div class='subtle'>Orders and revenue trend</div>", unsafe_allow_html=True)
        chart_df = get_sales_series(14)
        if not chart_df.empty:
            fig = px.line(chart_df, x="Date", y="Revenue", markers=True)
            fig.update_layout(height=360, margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data found.")

    with right:
        st.markdown("<div class='panel-title'>Top Categories</div><div class='subtle'>Product category split</div>", unsafe_allow_html=True)
        cat_df = top_categories()
        if not cat_df.empty:
            fig = px.pie(cat_df, names="Category", values="Products", hole=0.62)
            fig.update_layout(height=360, margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data found.")

    st.write("")
    st.markdown("<div class='panel-title'>Recent Orders</div>", unsafe_allow_html=True)
    st.dataframe(get_orders_df(8), use_container_width=True, hide_index=True)


def orders_page() -> None:
    page_header("Orders", "View, filter and export store orders")
    df = get_orders_df(80)
    if df.empty:
        st.warning("No orders found.")
        return

    f1, f2, f3 = st.columns(3)
    with f1:
        status = st.selectbox("Order Status", ["All"] + sorted(df["Order Status"].dropna().astype(str).unique().tolist()))
    with f2:
        payment = st.selectbox("Payment", ["All"] + sorted(df["Payment"].dropna().astype(str).unique().tolist()))
    with f3:
        search = st.text_input("Search", placeholder="Order ID, customer, city, SKU")

    view = df.copy()
    if status != "All":
        view = view[view["Order Status"].astype(str) == status]
    if payment != "All":
        view = view[view["Payment"].astype(str) == payment]
    if search:
        mask = view.astype(str).apply(lambda row: row.str.contains(search, case=False, na=False).any(), axis=1)
        view = view[mask]

    st.download_button("Download Orders CSV", view.to_csv(index=False).encode("utf-8"), "orders.csv", "text/csv")
    st.dataframe(view, use_container_width=True, height=620, hide_index=True)


def inventory_page() -> None:
    page_header("Inventory", "Track products, SKU and stock levels")
    df = get_products_df()
    if df.empty:
        st.warning("No products found.")
        return

    c1, c2, c3 = st.columns(3)
    summary = product_summary()
    with c1:
        metric_card("Products", number(summary["products"]), "Total SKUs", "good")
    with c2:
        metric_card("Low Stock", number(summary["low_stock"]), "Restock soon", "warn")
    with c3:
        metric_card("Out of Stock", number(summary["out_stock"]), "Urgent", "bad")

    status = st.selectbox("Stock Filter", ["All"] + sorted(df["Status"].dropna().astype(str).unique().tolist()))
    view = df if status == "All" else df[df["Status"].astype(str) == status]
    st.dataframe(view, use_container_width=True, height=620, hide_index=True)


def shipping_page() -> None:
    page_header("Shipping", "Shiprocket workflow and shipment status")
    df = get_shipments_df()
    if df.empty:
        st.info("Shipping data will appear here after Shiprocket integration.")
        return
    status = st.selectbox("Shipment Status", ["All"] + sorted(df["Status"].dropna().astype(str).unique().tolist()))
    view = df if status == "All" else df[df["Status"].astype(str) == status]
    st.dataframe(view, use_container_width=True, height=620, hide_index=True)


def returns_page() -> None:
    page_header("Returns / RTO", "Track failed delivery, RTO and returns")
    df = get_orders_df(80)
    if df.empty:
        st.info("No return data found.")
        return
    mask = df["Order Status"].astype(str).str.contains("rto|failed|cancelled|return", case=False, na=False)
    st.dataframe(df[mask], use_container_width=True, height=620, hide_index=True)


def reports_page() -> None:
    page_header("Reports", "Daily sales, payment and category reports")
    sales = get_sales_series(30)
    if not sales.empty:
        st.dataframe(sales, use_container_width=True, hide_index=True)
        st.download_button("Download Sales Report", sales.to_csv(index=False).encode("utf-8"), "sales_report.csv", "text/csv")
    else:
        st.info("No report data found.")


def settings_page() -> None:
    page_header("Settings", "Current dashboard configuration")
    st.code(f"API_PROVIDER={settings.api_provider}\nWC_SITE_URL={settings.wc_site_url}\nCACHE_TTL_SECONDS={settings.cache_ttl_seconds}")
    st.info("API keys are read from Streamlit Secrets or .env. Never commit real keys to GitHub.")


if page == "Dashboard":
    dashboard_page()
elif page == "Orders":
    orders_page()
elif page == "Inventory":
    inventory_page()
elif page == "Shipping":
    shipping_page()
elif page == "Returns":
    returns_page()
elif page == "Reports":
    reports_page()
else:
    settings_page()
