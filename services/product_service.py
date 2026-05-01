from __future__ import annotations

import pandas as pd
import streamlit as st

from config import settings
from services.provider import get_data_adapter


@st.cache_data(ttl=settings.cache_ttl_seconds, show_spinner=False)
def get_products() -> list[dict]:
    return get_data_adapter().fetch_products()


def get_products_df() -> pd.DataFrame:
    return pd.DataFrame(get_products())


def product_summary() -> dict:
    df = get_products_df()
    if df.empty:
        return {"products": 0, "low_stock": 0, "out_stock": 0}
    status = df.get("Status").astype(str)
    return {
        "products": int(len(df)),
        "low_stock": int(status.str.contains("Low", case=False, na=False).sum()),
        "out_stock": int(status.str.contains("Out", case=False, na=False).sum()),
    }
