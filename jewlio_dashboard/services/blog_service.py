from __future__ import annotations

import pandas as pd
import streamlit as st

from config import settings
from services.provider import get_data_adapter


@st.cache_data(ttl=settings.cache_ttl_seconds, show_spinner=False)
def get_posts(limit: int = 50) -> list[dict]:
    adapter = get_data_adapter()
    if hasattr(adapter, "fetch_posts"):
        return adapter.fetch_posts(limit)
    return []


def get_posts_df(limit: int = 50) -> pd.DataFrame:
    return pd.DataFrame(get_posts(limit))
