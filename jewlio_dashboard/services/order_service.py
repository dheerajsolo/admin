from __future__ import annotations

import pandas as pd
import streamlit as st

from config import settings
from services.provider import get_data_adapter
from utils.formatters import to_float
from utils.helpers import find_col


@st.cache_data(ttl=settings.cache_ttl_seconds, show_spinner=False)
def get_orders(limit: int = 100) -> list[dict]:
    adapter = get_data_adapter()
    try:
        return adapter.fetch_orders(limit)
    except TypeError:
        return adapter.fetch_orders()


def get_orders_df(limit: int = 100) -> pd.DataFrame:
    return pd.DataFrame(get_orders(limit))


def get_normalized_orders_df(limit: int = 100) -> pd.DataFrame:
    df = get_orders_df(limit)

    columns = [
        "order_id", "date", "customer", "phone", "city", "product", "sku", "qty",
        "payment_method", "total", "paid_amount", "cod_due", "status", "shipping_status",
    ]

    if df.empty:
        return pd.DataFrame(columns=columns)

    order_col = find_col(df, ["order_id", "id", "Order ID", "Order"])
    date_col = find_col(df, ["date", "date_created", "order_date", "Date"])
    customer_col = find_col(df, ["customer", "customer_name", "name", "Customer"])
    phone_col = find_col(df, ["phone", "billing_phone", "Phone"])
    city_col = find_col(df, ["city", "billing_city", "City"])
    product_col = find_col(df, ["product", "products", "Product"])
    sku_col = find_col(df, ["sku", "SKU"])
    qty_col = find_col(df, ["qty", "quantity", "Qty"])
    payment_col = find_col(df, ["payment_method", "payment_method_title", "Payment Method", "Payment"])
    total_col = find_col(df, ["total", "order_total", "amount", "total_amount", "Total", "Amount"])
    paid_col = find_col(df, ["paid_amount", "Paid Amount", "paid", "Paid"])
    cod_col = find_col(df, ["cod_due", "COD Due", "remaining_cod", "Remaining COD", "collectable_amount"])
    status_col = find_col(df, ["status", "order_status", "Order Status", "Status"])
    shipping_col = find_col(df, ["shipping_status", "Shipping Status", "shipment_status"])

    clean = pd.DataFrame()
    clean["order_id"] = df[order_col] if order_col else ""
    clean["date"] = df[date_col] if date_col else ""
    clean["customer"] = df[customer_col] if customer_col else ""
    clean["phone"] = df[phone_col] if phone_col else ""
    clean["city"] = df[city_col] if city_col else ""
    clean["product"] = df[product_col] if product_col else ""
    clean["sku"] = df[sku_col] if sku_col else ""
    clean["qty"] = df[qty_col] if qty_col else ""
    clean["payment_method"] = df[payment_col] if payment_col else ""
    clean["total"] = df[total_col].apply(to_float) if total_col else 0.0
    clean["paid_amount"] = df[paid_col].apply(to_float) if paid_col else 0.0
    clean["cod_due"] = df[cod_col].apply(to_float) if cod_col else 0.0
    clean["status"] = df[status_col] if status_col else ""
    clean["shipping_status"] = df[shipping_col] if shipping_col else ""

    return clean
