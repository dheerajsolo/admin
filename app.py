from __future__ import annotations

import streamlit as st
from textwrap import dedent

from config import settings
from components.sidebar import render_sidebar

from modules.overview.page import render_overview_page
from modules.orders.page import render_orders_page
from modules.inventory.page import render_inventory_page
from modules.shipping.page import render_shipping_page
from modules.blog.page import render_blog_page
from modules.email_support.page import render_email_support_page
from modules.push_notifications.page import render_push_notifications_page
from modules.reports.page import render_reports_page
from modules.settings.page import render_settings_page


st.set_page_config(
    page_title="Jewlio Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


def html(content: str) -> None:
    st.markdown(dedent(content), unsafe_allow_html=True)


def load_css() -> None:
    html(
        """
        <style>
        :root {
            --bg: #EEEEEE;
            --primary: #02224F;
            --muted: #BFC9D1;
            --surface: #EAEFEF;
            --sidebar: #25343F;
            --text: #25343F;
            --soft-text: #5E6B75;
            --border: #D6DEE4;
            --white: #FFFFFF;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        .stApp {
            background: var(--bg) !important;
            color: var(--text) !important;
        }

        .block-container {
            padding-top: 42px !important;
            padding-left: 3.5rem !important;
            padding-right: 3.5rem !important;
            max-width: 1500px !important;
        }

        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        [data-testid="stSidebar"] {
            background: var(--sidebar) !important;
            min-width: 250px !important;
            max-width: 250px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: var(--sidebar) !important;
            padding: 34px 24px !important;
        }

        [data-testid="stSidebar"] * {
            color: #EAEFEF !important;
        }

        [data-testid="stSidebar"] .stButton {
            margin-bottom: 6px !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            height: 42px !important;
            text-align: left !important;
            justify-content: flex-start !important;
            background: transparent !important;
            border: 0 !important;
            border-radius: 12px !important;
            color: #EAEFEF !important;
            font-weight: 700 !important;
            box-shadow: none !important;
            padding: 8px 14px !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(234, 239, 239, 0.12) !important;
            color: #FFFFFF !important;
        }

        .sidebar-brand {
            padding-bottom: 24px;
            border-bottom: 1px solid rgba(234,239,239,0.15);
            margin-bottom: 24px;
        }

        .sidebar-title {
            font-size: 28px;
            font-weight: 900;
            color: #FFFFFF !important;
            margin-bottom: 6px;
            line-height: 1.1;
        }

        .sidebar-subtitle {
            font-size: 13px;
            color: #BFC9D1 !important;
        }

        .sidebar-section {
            margin: 22px 0 10px 0;
            font-size: 11px;
            font-weight: 900;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #BFC9D1 !important;
        }

        .page-title {
            color: var(--text);
            font-size: 24px;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .page-subtitle {
            color: var(--soft-text);
            font-size: 14px;
        }

        .search-box {
            background: #F7F9FA;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 13px 18px;
            color: var(--soft-text);
            font-size: 14px;
        }

        .metric-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 20px;
            min-height: 138px;
            box-shadow: 0 1px 3px rgba(2, 34, 79, 0.06);
        }

        .metric-card.dark {
            background: var(--primary);
            border-color: var(--primary);
        }

        .metric-label {
            color: var(--soft-text);
            font-size: 14px;
            font-weight: 800;
            margin-bottom: 18px;
        }

        .metric-card.dark .metric-label {
            color: #EAEFEF;
        }

        .metric-value {
            color: var(--text);
            font-size: 27px;
            font-weight: 900;
            margin-bottom: 18px;
        }

        .metric-card.dark .metric-value {
            color: #FFFFFF;
        }

        .metric-badge {
            display: inline-block;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            background: #E4EAEE;
            color: #25343F;
        }

        .metric-badge.success {
            background: #DCEFE4;
            color: #227A4D;
        }

        .metric-badge.warn {
            background: #F4E7C8;
            color: #9A6A00;
        }

        .panel-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(2, 34, 79, 0.06);
            margin-bottom: 0;
        }

        .panel-card.chart-head {
            border-radius: 20px 20px 0 0;
            border-bottom: 0;
            margin-bottom: 0;
        }

        .panel-title {
            color: var(--text);
            font-size: 17px;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .panel-subtitle {
            color: var(--soft-text);
            font-size: 13px;
        }

        .table-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(2, 34, 79, 0.06);
        }

        .table-title {
            color: var(--text);
            font-size: 17px;
            font-weight: 900;
            margin-bottom: 4px;
        }

        .table-subtitle {
            color: var(--soft-text);
            font-size: 13px;
            margin-bottom: 12px;
        }

        [data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
        }

        .stProgress > div > div > div > div {
            background-color: #02224F !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 20px !important;
            border-color: #D6DEE4 !important;
            background: #FFFFFF !important;
            box-shadow: 0 1px 3px rgba(2, 34, 79, 0.06);
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }

            [data-testid="stSidebar"] {
                min-width: 220px !important;
                max-width: 220px !important;
            }
        }
        </style>
        """
    )


def check_login() -> bool:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.markdown("### Dashboard Login")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if password == settings.app_password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect password")

    return False


def render_page(page_name: str) -> None:
    if page_name == "Overview":
        render_overview_page()
    elif page_name == "Orders":
        render_orders_page()
    elif page_name == "Inventory":
        render_inventory_page()
    elif page_name == "Shipping":
        render_shipping_page()
    elif page_name == "Blog":
        render_blog_page()
    elif page_name == "Email Support":
        render_email_support_page()
    elif page_name == "Push Notifications":
        render_push_notifications_page()
    elif page_name == "Reports":
        render_reports_page()
    elif page_name == "Settings":
        render_settings_page()
    else:
        render_overview_page()


def main() -> None:
    load_css()

    if not check_login():
        return

    selected_page = render_sidebar()

    render_page(selected_page)


if __name__ == "__main__":
    main()
