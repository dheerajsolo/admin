from __future__ import annotations

import requests
from requests import Session
import streamlit as st

from config import settings
from utils.formatters import to_float


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


def _wp_get(endpoint: str, params: dict | None = None):
    url = f"{settings.wc_site_url}/wp-json/wp/v2/{endpoint.lstrip('/')}"
    response = requests.get(url, params=params or {}, timeout=25)
    response.raise_for_status()
    return response.json()


def _meta_float(order: dict, key: str) -> float:
    for meta in order.get("meta_data", []) or []:
        if meta.get("key") == key:
            return to_float(meta.get("value"))
    return 0.0


def fetch_orders(limit: int = 100) -> list[dict]:
    raw_orders = _get(
        "orders",
        {
            "per_page": min(int(limit or 100), 100),
            "orderby": "date",
            "order": "desc",
        },
    )

    clean: list[dict] = []

    for order in raw_orders:
        billing = order.get("billing", {}) or {}
        items = order.get("line_items", []) or []

        product_names = ", ".join([str(i.get("name", "")).strip() for i in items if i.get("name")])
        skus = ", ".join([str(i.get("sku", "")).strip() for i in items if i.get("sku")])
        qty = sum(int(i.get("quantity") or 0) for i in items)

        total = to_float(order.get("total"))
        paid = _meta_float(order, "_woobooster_partial_cod_paid_amount")
        cod_due = _meta_float(order, "_woobooster_partial_cod_remaining_amount")

        if cod_due == 0 and paid > 0:
            cod_due = max(total - paid, 0)

        clean.append(
            {
                "order_id": order.get("id"),
                "date": str(order.get("date_created", ""))[:10],
                "customer": f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip() or "-",
                "phone": billing.get("phone", "-"),
                "city": billing.get("city", "-"),
                "product": product_names or "-",
                "sku": skus or "-",
                "qty": qty,
                "payment_method": order.get("payment_method_title") or order.get("payment_method") or "-",
                "total": total,
                "paid_amount": paid,
                "cod_due": cod_due,
                "status": order.get("status", "-"),
                "shipping_status": "-",
            }
        )

    return clean


def fetch_products(limit: int = 100) -> list[dict]:
    raw_products = _get(
        "products",
        {
            "per_page": min(int(limit or 100), 100),
            "orderby": "date",
            "order": "desc",
        },
    )

    rows: list[dict] = []

    for product in raw_products:
        stock = product.get("stock_quantity")
        stock_num = int(stock or 0)

        stock_status = product.get("stock_status") or ""
        categories = product.get("categories", []) or []
        category_text = ", ".join([str(c.get("name", "")).strip() for c in categories if c.get("name")])

        price = product.get("sale_price") or product.get("price") or product.get("regular_price") or 0

        if stock_status == "outofstock":
            display_status = "Out of Stock"
        elif stock_num <= settings.low_stock_threshold:
            display_status = "Low Stock"
        else:
            display_status = "In Stock"

        rows.append(
            {
                "product_id": product.get("id"),
                "name": product.get("name", "-"),
                "sku": product.get("sku", "-"),
                "category": category_text or "Uncategorized",
                "price": to_float(price),
                "stock_quantity": stock_num,
                "stock_status": stock_status,
                "status": display_status,
                "regular_price": to_float(product.get("regular_price")),
                "sale_price": to_float(product.get("sale_price") or product.get("price")),
                "total_sold": int(product.get("total_sales") or 0),
            }
        )

    return rows


def fetch_posts(limit: int = 50) -> list[dict]:
    posts = _wp_get(
        "posts",
        {
            "per_page": min(int(limit or 50), 100),
            "orderby": "date",
            "order": "desc",
            "status": "publish,draft",
        },
    )

    rows = []
    for post in posts:
        title = post.get("title", {}).get("rendered", "")
        rows.append(
            {
                "post_id": post.get("id"),
                "title": title,
                "status": post.get("status", "-"),
                "date": str(post.get("date", ""))[:10],
                "category": "-",
            }
        )
    return rows
