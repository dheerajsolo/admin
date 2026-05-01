from __future__ import annotations

import pandas as pd
import streamlit as st


def render_table(df: pd.DataFrame, empty_message: str = "No data found.") -> None:
    if df.empty:
        st.info(empty_message)
        return
    st.dataframe(df, use_container_width=True, hide_index=True)
