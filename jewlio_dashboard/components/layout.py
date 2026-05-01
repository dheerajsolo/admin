from __future__ import annotations

from textwrap import dedent
import streamlit as st


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
            --success: #0C8F5A;
            --warning: #9A6A00;
            --danger: #B42318;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            background: var(--bg) !important;
            color: var(--text) !important;
        }

        .block-container {
            padding-top: 28px !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 1480px !important;
        }

        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        [data-testid="stSidebar"] {
            background: #0C1715 !important;
            min-width: 260px !important;
            max-width: 260px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: #0C1715 !important;
            padding: 24px 18px !important;
        }

        [data-testid="stSidebar"] * {
            color: #EAEFEF !important;
        }

        [data-testid="stSidebar"] .stButton {
            margin-bottom: 5px !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            height: 41px !important;
            text-align: left !important;
            justify-content: flex-start !important;
            background: transparent !important;
            border: 0 !important;
            border-radius: 11px !important;
            color: #BFC9D1 !important;
            font-weight: 700 !important;
            box-shadow: none !important;
            padding: 8px 13px !important;
            font-size: 14px !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(234, 239, 239, 0.09) !important;
            color: #FFFFFF !important;
        }

        .sidebar-brand {
            padding: 8px 4px 22px 4px;
            border-bottom: 1px solid rgba(234,239,239,0.10);
            margin-bottom: 18px;
        }

        .sidebar-title {
            font-size: 22px;
            font-weight: 900;
            color: #FFFFFF !important;
            margin-bottom: 3px;
            letter-spacing: -0.3px;
        }

        .sidebar-subtitle {
            font-size: 10px;
            color: #BFC9D1 !important;
            text-transform: uppercase;
            letter-spacing: 1.6px;
        }

        .sidebar-section {
            margin: 18px 0 8px 4px;
            font-size: 10px;
            font-weight: 900;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            color: rgba(191,201,209,0.72) !important;
        }

        .sidebar-footer {
            border-top: 1px solid rgba(234,239,239,0.10);
            margin-top: 24px;
            padding-top: 18px;
        }

        .topbar {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 18px;
        }

        .search-box {
            background: #F7F9FA;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 12px 16px;
            color: var(--soft-text);
            font-size: 14px;
            max-width: 360px;
        }

        .action-button {
            background: var(--primary);
            color: #FFFFFF;
            padding: 12px 16px;
            border-radius: 12px;
            font-weight: 800;
            font-size: 13px;
            text-align: center;
        }

        .page-title {
            color: #111827;
            font-size: 28px;
            font-weight: 900;
            margin-bottom: 4px;
            letter-spacing: -0.8px;
        }

        .page-subtitle {
            color: var(--soft-text);
            font-size: 14px;
            margin-bottom: 16px;
        }

        .metric-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px;
            min-height: 142px;
            box-shadow: 0 8px 20px rgba(2, 34, 79, 0.04);
        }

        .metric-label {
            color: var(--soft-text);
            font-size: 13px;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .metric-value {
            color: #111827;
            font-size: 25px;
            font-weight: 900;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }

        .metric-note {
            color: var(--soft-text);
            font-size: 12px;
            font-weight: 700;
        }

        .metric-good {
            color: #0C8F5A;
            font-weight: 900;
        }

        .metric-warn {
            color: #B42318;
            font-weight: 900;
        }

        .sparkline {
            margin-top: 11px;
            height: 18px;
            border-radius: 99px;
            background: linear-gradient(90deg, rgba(2,34,79,0.10), rgba(191,201,209,0.45));
        }

        .panel-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 8px 20px rgba(2, 34, 79, 0.04);
            margin-bottom: 16px;
        }

        .panel-title {
            color: #111827;
            font-size: 17px;
            font-weight: 900;
            margin-bottom: 4px;
        }

        .panel-subtitle {
            color: var(--soft-text);
            font-size: 13px;
            margin-bottom: 10px;
        }

        .table-title {
            color: #111827;
            font-size: 17px;
            font-weight: 900;
            margin-bottom: 4px;
        }

        .table-subtitle {
            color: var(--soft-text);
            font-size: 13px;
            margin-bottom: 12px;
        }

        .status-pill {
            display: inline-block;
            padding: 7px 11px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            background: #EAEFEF;
            color: #25343F;
        }

        .status-success {
            background: #DCEFE4;
            color: #0C8F5A;
        }

        .status-warning {
            background: #F4E7C8;
            color: #9A6A00;
        }

        .status-danger {
            background: #FDE2E0;
            color: #B42318;
        }

        [data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px !important;
            border-color: #D6DEE4 !important;
            background: #FFFFFF !important;
            box-shadow: 0 8px 20px rgba(2, 34, 79, 0.04);
        }

        .stProgress > div > div > div > div {
            background-color: #02224F !important;
        }

        .login-shell {
            max-width: 420px;
            margin: 80px auto 0 auto;
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 26px;
            box-shadow: 0 8px 20px rgba(2, 34, 79, 0.08);
        }

        .login-title {
            font-size: 26px;
            font-weight: 900;
            color: #111827;
            margin-bottom: 4px;
        }

        .login-subtitle {
            font-size: 14px;
            color: var(--soft-text);
            margin-bottom: 14px;
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }

            [data-testid="stSidebar"] {
                min-width: 230px !important;
                max-width: 230px !important;
            }
        }
        </style>
        """
    )
