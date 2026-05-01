from __future__ import annotations

import pandas as pd
import streamlit as st

from config import settings
from services.provider import get_data_adapter
from utils.formatters import to_float
from utils.helpers import find_col


@st.cache_data(ttl=settings.cache_ttl_seconds, show_spinner=False)
def get_products(limit: int = 100) -> list[dict]:
    adapter = get_data_adapter()
    try:
        return adapter.fetch_products(limit)
    except TypeError:
        return adapter.fetch_products()


def get_products_df(limit: int = 100) -> pd.DataFrame:
    return pd.DataFrame(get_products(limit))


def get_normalized_products_df(limit: int = 100) -> pd.DataFrame:
    df = get_products_df(limit)

    columns = [
        "product_id", "name", "sku", "category", "price", "stock_quantity",
        "stock_status", "status", "total_sold",
    ]

    if df.empty:
        return pd.DataFrame(columns=columns)

    id_col = find_col(df, ["product_id", "id", "ID", "Product ID"])
    name_col = find_col(df, ["name", "product_name", "Product", "Name"])
    sku_col = find_col(df, ["sku", "SKU"])
    category_col = find_col(df, ["category", "categories", "Category"])
    price_col = find_col(df, ["price", "regular_price", "sale_price", "Price", "Sale Price"])
    stock_qty_col = find_col(df, ["stock_quantity", "stock", "Stock", "qty", "quantity"])
    stock_status_col = find_col(df, ["stock_status", "Stock Status", "stockStatus"])
    status_col = find_col(df, ["status", "Status"])
    sold_col = find_col(df, ["total_sold", "Total Sold", "total_sales"])

    clean = pd.DataFrame()
    clean["product_id"] = df[id_col] if id_col else ""
    clean["name"] = df[name_col] if name_col else ""
    clean["sku"] = df[sku_col] if sku_col else ""
    clean["category"] = df[category_col] if category_col else "Uncategorized"
    clean["price"] = df[price_col].apply(to_float) if price_col else 0.0
    clean["stock_quantity"] = df[stock_qty_col].apply(to_float) if stock_qty_col else 0.0
    clean["stock_status"] = df[stock_status_col] if stock_status_col else ""
    clean["status"] = df[status_col] if status_col else ""
    clean["total_sold"] = df[sold_col] if sold_col else 0

    return clean
