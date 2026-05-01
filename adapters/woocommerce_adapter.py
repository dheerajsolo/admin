from __future__ import annotations

import requests
from requests import Session
import streamlit as st

from config import settings


@st.cache_resource(show_spinner=False)
def _session() -> Session:
    s = requests.Session()
    s.auth = (settings.wc_consumer_key, settings.wc_consumer_secret)
    s.headers.update({"User-Agent": "JewlioOpsDashboard/1.0"})
    return s


def _get(endpoint: str, params: dict | None = None):
    if not settings.wc_consumer_key or not settings.wc_consumer_secret:
        raise RuntimeError("WooCommerce keys missing. Add secrets first or use API_PROVIDER=demo.")
    url = f"{settings.wc_site_url}/wp-json/wc/v3/{endpoint.lstrip('/')}"
    response = _session().get(url, params=params or {}, timeout=25)
    response.raise_for_status()
    return response.json()


def fetch_orders(limit: int = 50) -> list[dict]:
    raw_orders = _get("orders", {"per_page": min(limit, 100), "orderby": "date", "order": "desc"})
    clean: list[dict] = []
    for order in raw_orders:
        billing = order.get("billing", {}) or {}
        items = order.get("line_items", []) or []
        product_names = ", ".join([i.get("name", "") for i in items])
        skus = ", ".join([i.get("sku", "") for i in items if i.get("sku")])
        total = float(order.get("total") or 0)
        paid = _meta_float(order, "_woobooster_partial_cod_paid_amount")
        cod_due = _meta_float(order, "_woobooster_partial_cod_remaining_amount")
        if cod_due == 0 and paid > 0:
            cod_due = max(total - paid, 0)
        clean.append({
            "Order ID": f"#{order.get('id')}",
            "Date": order.get("date_created", "")[:10],
            "Customer": f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip() or "-",
            "Phone": billing.get("phone", "-"),
            "City": billing.get("city", "-"),
            "Product": product_names,
            "SKU": skus,
            "Qty": sum(int(i.get("quantity") or 0) for i in items),
            "Payment": order.get("payment_method_title") or order.get("payment_method") or "-",
            "Total": total,
            "Paid": paid,
            "COD Due": cod_due,
            "Order Status": order.get("status", "-"),
            "Shipping Status": "-",
        })
    return clean


def fetch_products() -> list[dict]:
    raw_products = _get("products", {"per_page": 100, "orderby": "date", "order": "desc"})
    rows: list[dict] = []
    for product in raw_products:
        stock = product.get("stock_quantity")
        stock_num = int(stock or 0)
        if product.get("stock_status") == "outofstock":
            status = "Out of Stock"
        elif stock_num <= 5:
            status = "Low Stock"
        else:
            status = "In Stock"
        rows.append({
            "SKU": product.get("sku", "-"),
            "Product": product.get("name", "-"),
            "Category": ", ".join([c.get("name", "") for c in product.get("categories", [])]),
            "Stock": stock_num,
            "Status": status,
            "Regular Price": product.get("regular_price") or 0,
            "Sale Price": product.get("sale_price") or product.get("price") or 0,
            "Total Sold": product.get("total_sales") or 0,
        })
    return rows


def _meta_float(order: dict, key: str) -> float:
    for meta in order.get("meta_data", []) or []:
        if meta.get("key") == key:
            try:
                return float(meta.get("value") or 0)
            except Exception:
                return 0.0
    return 0.0
