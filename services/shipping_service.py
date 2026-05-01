from __future__ import annotations

import pandas as pd
import streamlit as st

from config import settings
from services.provider import get_data_adapter


@st.cache_data(ttl=settings.cache_ttl_seconds, show_spinner=False)
def get_shipments() -> list[dict]:
    adapter = get_data_adapter()
    if hasattr(adapter, "fetch_shipments"):
        return adapter.fetch_shipments()
    return []


def get_shipments_df() -> pd.DataFrame:
    return pd.DataFrame(get_shipments())
