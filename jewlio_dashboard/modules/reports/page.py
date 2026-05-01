from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from services.order_service import get_normalized_orders_df
from utils.formatters import money, to_float


def render_reports_page() -> None:
    st.markdown('<div class="page-title">Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Sales and operations reporting based on available order data.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df = get_normalized_orders_df(100)

    if df.empty:
        st.info("No report data found.")
        return

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["total"] = df["total"].apply(to_float)

    city_report = df.groupby("city", as_index=False)["total"].sum().sort_values("total", ascending=False).head(10)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=city_report["city"], y=city_report["total"], marker_color="#02224F"))
    fig.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="City",
        yaxis_title="Revenue",
        font=dict(color="#25343F"),
    )

    st.plotly_chart(fig, use_container_width=True)

    city_report["total"] = city_report["total"].apply(money)
    st.dataframe(city_report, use_container_width=True, hide_index=True)
