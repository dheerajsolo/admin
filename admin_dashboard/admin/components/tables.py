from __future__ import annotations

import pandas as pd
import streamlit as st


def show_table(data, height: int = 520, hide_index: bool = True) -> None:
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, height=height, hide_index=hide_index)
