from __future__ import annotations

import pandas as pd
import streamlit as st

from config import settings
from services.provider import get_data_adapter


def _to_float(value) -> float:
    try:
        if value is None:
            return 0.0
        return float(str(value).replace(",", "").replace("₹", "").strip())
    except Exception:
        return 0.0


def _find_col(df: pd.DataFrame, possible_names: list[str]) -> str | None:
    for name in possible_names:
        if name in df.columns:
            return name
    return None


@st.cache_data(ttl=settings.cache_ttl_seconds, show_spinner=False)
def get_products(limit: int = 100) -> list[dict]:
    """
    Fetch products from active data adapter.

    Compatible with both:
    - adapter.fetch_products()
    - adapter.fetch_products(limit)
    """
    adapter = get_data_adapter()

    try:
        return adapter.fetch_products(limit)
    except TypeError:
        return adapter.fetch_products()


def get_products_df(limit: int = 100) -> pd.DataFrame:
    return pd.DataFrame(get_products(limit))


def get_normalized_products_df(limit: int = 100) -> pd.DataFrame:
    """
    Standard product format for dashboard.
    This keeps UI independent from WooCommerce/demo/raw API column names.
    """
    df = get_products_df(limit)

    columns = [
        "product_id",
        "name",
        "sku",
        "category",
        "price",
        "stock_quantity",
        "stock_status",
        "status",
    ]

    if df.empty:
        return pd.DataFrame(columns=columns)

    id_col = _find_col(df, ["product_id", "id", "ID", "Product ID"])
    name_col = _find_col(df, ["name", "product_name", "Product", "Name"])
    sku_col = _find_col(df, ["sku", "SKU"])
    category_col = _find_col(df, ["category", "categories", "Category"])
    price_col = _find_col(df, ["price", "regular_price", "sale_price", "Price"])
    stock_qty_col = _find_col(df, ["stock_quantity", "stock", "Stock", "qty", "quantity"])
    stock_status_col = _find_col(df, ["stock_status", "Stock Status", "stockStatus"])
    status_col = _find_col(df, ["status", "Status"])

    clean = pd.DataFrame()
    clean["product_id"] = df[id_col] if id_col else ""
    clean["name"] = df[name_col] if name_col else ""
    clean["sku"] = df[sku_col] if sku_col else ""
    clean["category"] = df[category_col] if category_col else "Uncategorized"
    clean["price"] = df[price_col].apply(_to_float) if price_col else 0.0
    clean["stock_quantity"] = df[stock_qty_col].apply(_to_float) if stock_qty_col else 0.0
    clean["stock_status"] = df[stock_status_col] if stock_status_col else ""
    clean["status"] = df[status_col] if status_col else ""

    return clean


def product_summary(limit: int = 100) -> dict:
    df = get_normalized_products_df(limit)

    if df.empty:
        return {
            "products": 0,
            "low_stock": 0,
            "out_stock": 0,
        }

    stock_qty = pd.to_numeric(df["stock_quantity"], errors="coerce").fillna(0)
    stock_status = df["stock_status"].astype(str).str.lower()
    status = df["status"].astype(str).str.lower()

    threshold = getattr(settings, "low_stock_threshold", 5)

    out_stock = int(
        ((stock_qty <= 0) | stock_status.str.contains("outofstock|out of stock", na=False)).sum()
    )

    low_stock = int(
        (
            (stock_qty > 0)
            & (stock_qty <= threshold)
            & ~stock_status.str.contains("outofstock|out of stock", na=False)
        ).sum()
    )

    # Fallback for demo data where Status has "Low" or "Out"
    if out_stock == 0:
        out_stock = int(status.str.contains("out", case=False, na=False).sum())

    if low_stock == 0:
        low_stock = int(status.str.contains("low", case=False, na=False).sum())

    return {
        "products": int(len(df)),
        "low_stock": low_stock,
        "out_stock": out_stock,
    }
