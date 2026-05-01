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
def get_orders(limit: int = 50) -> list[dict]:
    """
    Fetch orders from active data adapter.

    Current mode:
    - demo adapter for demo data
    - woocommerce adapter for live read-only WooCommerce data
    """
    return get_data_adapter().fetch_orders(limit)


def get_orders_df(limit: int = 50) -> pd.DataFrame:
    return pd.DataFrame(get_orders(limit))


def get_normalized_orders_df(limit: int = 50) -> pd.DataFrame:
    """
    Standard order format for dashboard.
    This keeps pages independent from WooCommerce/demo/raw API column names.
    """
    df = get_orders_df(limit)

    columns = [
        "order_id",
        "date",
        "customer",
        "phone",
        "city",
        "product",
        "sku",
        "qty",
        "payment_method",
        "total",
        "paid_amount",
        "cod_due",
        "status",
    ]

    if df.empty:
        return pd.DataFrame(columns=columns)

    order_col = _find_col(df, ["order_id", "id", "Order ID", "Order"])
    date_col = _find_col(df, ["date", "date_created", "order_date", "Date"])
    customer_col = _find_col(df, ["customer", "customer_name", "name", "Customer"])
    phone_col = _find_col(df, ["phone", "billing_phone", "Phone"])
    city_col = _find_col(df, ["city", "billing_city", "City"])
    product_col = _find_col(df, ["product", "products", "Product"])
    sku_col = _find_col(df, ["sku", "SKU"])
    qty_col = _find_col(df, ["qty", "quantity", "Qty"])
    payment_col = _find_col(df, ["payment_method", "payment_method_title", "Payment Method", "Payment"])
    total_col = _find_col(df, ["total", "order_total", "amount", "total_amount", "Total", "Amount"])
    paid_col = _find_col(df, ["paid_amount", "Paid Amount", "paid", "Paid"])
    cod_col = _find_col(df, ["cod_due", "COD Due", "remaining_cod", "Remaining COD", "collectable_amount"])
    status_col = _find_col(df, ["status", "order_status", "Order Status", "Status"])

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
    clean["total"] = df[total_col].apply(_to_float) if total_col else 0.0
    clean["paid_amount"] = df[paid_col].apply(_to_float) if paid_col else 0.0
    clean["cod_due"] = df[cod_col].apply(_to_float) if cod_col else 0.0
    clean["status"] = df[status_col] if status_col else ""

    return clean


def order_summary(limit: int = 80) -> dict:
    df = get_normalized_orders_df(limit)

    if df.empty:
        return {
            "sales": 0.0,
            "orders": 0,
            "pending": 0,
            "cod_due": 0.0,
            "rto": 0,
        }

    status = df["status"].astype(str)

    pending = int(
        status.str.contains("processing|pending|on-hold|hold", case=False, na=False).sum()
    )

    rto = int(
        status.str.contains("rto|failed|cancelled|canceled|refunded", case=False, na=False).sum()
    )

    return {
        "sales": float(pd.to_numeric(df["total"], errors="coerce").fillna(0).sum()),
        "orders": int(len(df)),
        "pending": pending,
        "cod_due": float(pd.to_numeric(df["cod_due"], errors="coerce").fillna(0).sum()),
        "rto": rto,
    }
