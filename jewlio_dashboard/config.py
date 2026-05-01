from __future__ import annotations

import os
from dataclasses import dataclass

try:
    import streamlit as st
except Exception:
    st = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def _get_secret(key: str, default: str = "") -> str:
    if st is not None:
        try:
            value = st.secrets.get(key)
            if value is not None:
                return str(value)
        except Exception:
            pass
    return os.getenv(key, default)


def _to_int(value: str, default: int) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return default


@dataclass(frozen=True)
class Settings:
    api_provider: str = _get_secret("API_PROVIDER", "demo").lower()
    app_password: str = _get_secret("APP_PASSWORD", "admin")

    wc_site_url: str = _get_secret("WC_SITE_URL", "https://jewlio.in").rstrip("/")
    wc_consumer_key: str = _get_secret("WC_CONSUMER_KEY", "")
    wc_consumer_secret: str = _get_secret("WC_CONSUMER_SECRET", "")

    shiprocket_email: str = _get_secret("SHIPROCKET_EMAIL", "")
    shiprocket_password: str = _get_secret("SHIPROCKET_PASSWORD", "")

    cache_ttl_seconds: int = _to_int(_get_secret("CACHE_TTL_SECONDS", "120"), 120)
    low_stock_threshold: int = _to_int(_get_secret("LOW_STOCK_THRESHOLD", "5"), 5)


settings = Settings()
