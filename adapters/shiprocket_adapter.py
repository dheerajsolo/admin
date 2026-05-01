from __future__ import annotations

import requests
import streamlit as st
from config import settings

SHIPROCKET_BASE_URL = "https://apiv2.shiprocket.in/v1/external"


@st.cache_data(ttl=60 * 20, show_spinner=False)
def get_token() -> str:
    if not settings.shiprocket_email or not settings.shiprocket_password:
        return ""
    response = requests.post(
        f"{SHIPROCKET_BASE_URL}/auth/login",
        json={"email": settings.shiprocket_email, "password": settings.shiprocket_password},
        timeout=25,
    )
    response.raise_for_status()
    return response.json().get("token", "")


def auth_headers() -> dict:
    token = get_token()
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}
