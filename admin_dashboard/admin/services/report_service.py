from __future__ import annotations

import pandas as pd
import streamlit as st

from config import settings
from services.provider import get_data_adapter
from services.order_service import get_orders_df


@st.cache_data(ttl=settings.cache_ttl_seconds, show_spinner=False)
def get_sales_series(days: int = 14) -> pd.DataFrame:
    adapter = get_data_adapter()
    if hasattr(adapter, "fetch_sales_series"):
        return pd.DataFrame(adapter.fetch_sales_series(days))

    orders = get_orders_df(100)
    if orders.empty or "Date" not in orders.columns:
        return pd.DataFrame(columns=["Date", "Orders", "Revenue"])
    grouped = orders.groupby("Date", as_index=False).agg(Orders=("Order ID", "count"), Revenue=("Total", "sum"))
    return grouped.tail(days)


def top_categories() -> pd.DataFrame:
    from services.product_service import get_products_df
    df = get_products_df()
    if df.empty or "Category" not in df.columns:
        return pd.DataFrame(columns=["Category", "Products"])
    return df.groupby("Category", as_index=False).size().rename(columns={"size": "Products"}).sort_values("Products", ascending=False)
