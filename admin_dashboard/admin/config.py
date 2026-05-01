from __future__ import annotations

import os
from dataclasses import dataclass

try:
    import streamlit as st
except Exception:  # pragma: no cover
    st = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def _get_secret(key: str, default: str = "") -> str:
    """Read from Streamlit secrets first, then environment variables."""
    if st is not None:
        try:
            value = st.secrets.get(key)  # type: ignore[attr-defined]
            if value is not None:
                return str(value)
        except Exception:
            pass
    return os.getenv(key, default)


@dataclass(frozen=True)
class Settings:
    api_provider: str = _get_secret("API_PROVIDER", "demo").lower()
    app_password: str = _get_secret("APP_PASSWORD", "admin")

    wc_site_url: str = _get_secret("WC_SITE_URL", "https://jewlio.in").rstrip("/")
    wc_consumer_key: str = _get_secret("WC_CONSUMER_KEY", "")
    wc_consumer_secret: str = _get_secret("WC_CONSUMER_SECRET", "")

    shiprocket_email: str = _get_secret("SHIPROCKET_EMAIL", "")
    shiprocket_password: str = _get_secret("SHIPROCKET_PASSWORD", "")

    cache_ttl_seconds: int = int(_get_secret("CACHE_TTL_SECONDS", "120") or 120)


settings = Settings()
