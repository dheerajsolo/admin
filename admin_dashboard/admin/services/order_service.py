from __future__ import annotations

import pandas as pd
import streamlit as st

from config import settings
from services.provider import get_data_adapter


@st.cache_data(ttl=settings.cache_ttl_seconds, show_spinner=False)
def get_orders(limit: int = 50) -> list[dict]:
    return get_data_adapter().fetch_orders(limit)


def get_orders_df(limit: int = 50) -> pd.DataFrame:
    return pd.DataFrame(get_orders(limit))


def order_summary() -> dict:
    df = get_orders_df(80)
    if df.empty:
        return {"sales": 0, "orders": 0, "pending": 0, "cod_due": 0, "rto": 0}
    status_col = df.get("Order Status")
    pending = int(status_col.astype(str).str.contains("processing|pending", case=False, na=False).sum()) if status_col is not None else 0
    rto = int(status_col.astype(str).str.contains("rto|failed|cancelled", case=False, na=False).sum()) if status_col is not None else 0
    return {
        "sales": float(pd.to_numeric(df.get("Total", 0), errors="coerce").fillna(0).sum()),
        "orders": int(len(df)),
        "pending": pending,
        "cod_due": float(pd.to_numeric(df.get("COD Due", 0), errors="coerce").fillna(0).sum()),
        "rto": rto,
    }
