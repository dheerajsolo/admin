from __future__ import annotations

import streamlit as st

from components.layout import load_css
from components.sidebar import render_sidebar
from controllers.auth_controller import render_login
from controllers.router import render_selected_page


st.set_page_config(
    page_title="Jewlio Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    load_css()

    if not render_login():
        return

    selected_page = render_sidebar()
    render_selected_page(selected_page)


if __name__ == "__main__":
    main()
