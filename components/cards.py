from __future__ import annotations

import streamlit as st


def metric_card(label: str, value: str, delta: str = "", tone: str = "good", dark: bool = False) -> None:
    dark_class = " dark" if dark else ""
    delta_html = f"<span class='metric-delta {tone}'>{delta}</span>" if delta else ""
    st.markdown(
        f"""
        <div class='metric-card{dark_class}'>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='main-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='subtle'>{subtitle}</div>", unsafe_allow_html=True)
    st.write("")


def panel_start(title: str, subtitle: str = "") -> None:
    sub = f"<div class='subtle'>{subtitle}</div>" if subtitle else ""
    st.markdown(f"<div class='panel'><div class='panel-title'>{title}</div>{sub}", unsafe_allow_html=True)


def panel_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)
