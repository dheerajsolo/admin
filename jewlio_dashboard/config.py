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


def _to_bool(value: str, default: bool = False) -> bool:
    text = str(value).strip().lower()

    if text in ["true", "1", "yes", "on"]:
        return True

    if text in ["false", "0", "no", "off"]:
        return False

    return default


@dataclass(frozen=True)
class Settings:
    app_name: str = _get_secret("APP_NAME", "Store Dashboard")
    brand_name: str = _get_secret("BRAND_NAME", "Store")
    app_password: str = _get_secret("APP_PASSWORD", "admin")

    api_provider: str = _get_secret("API_PROVIDER", "demo").lower()

    wc_site_url: str = _get_secret("WC_SITE_URL", "").rstrip("/")
    wc_consumer_key: str = _get_secret("WC_CONSUMER_KEY", "")
    wc_consumer_secret: str = _get_secret("WC_CONSUMER_SECRET", "")

    cache_ttl_seconds: int = _to_int(_get_secret("CACHE_TTL_SECONDS", "120"), 120)
    low_stock_threshold: int = _to_int(_get_secret("LOW_STOCK_THRESHOLD", "5"), 5)

    gmail_enabled: bool = _to_bool(_get_secret("GMAIL_ENABLED", "false"), False)
    gmail_email: str = _get_secret("GMAIL_EMAIL", "")
    gmail_app_password: str = _get_secret("GMAIL_APP_PASSWORD", "")

    shiprocket_enabled: bool = _to_bool(_get_secret("SHIPROCKET_ENABLED", "false"), False)
    shiprocket_email: str = _get_secret("SHIPROCKET_EMAIL", "")
    shiprocket_password: str = _get_secret("SHIPROCKET_PASSWORD", "")

    push_enabled: bool = _to_bool(_get_secret("PUSH_ENABLED", "false"), False)

    demo_users_enabled: bool = _to_bool(_get_secret("DEMO_USERS_ENABLED", "true"), True)


settings = Settings()


DEMO_USERS = {
    "admin@store.com": {
        "password": "admin",
        "role": "Admin",
        "name": "Admin User",
    },
    "orders@store.com": {
        "password": "orders",
        "role": "Orders Staff",
        "name": "Orders Staff",
    },
    "inventory@store.com": {
        "password": "inventory",
        "role": "Inventory Staff",
        "name": "Inventory Staff",
    },
    "blog@store.com": {
        "password": "blog",
        "role": "Blog Staff",
        "name": "Blog Staff",
    },
    "email@store.com": {
        "password": "email",
        "role": "Email Support",
        "name": "Email Support",
    },
    "seo@store.com": {
        "password": "seo",
        "role": "SEO Staff",
        "name": "SEO Staff",
    },
    "viewer@store.com": {
        "password": "viewer",
        "role": "Viewer",
        "name": "Viewer",
    },
}


ROLE_ACCESS = {
    "Admin": [
        "Overview",
        "Orders",
        "Inventory",
        "Shipping",
        "Coupons",
        "Reviews",
        "Blog",
        "Email Support",
        "SEO",
        "Push Notifications",
        "Reports",
        "Users",
        "Settings",
    ],
    "Orders Staff": [
        "Overview",
        "Orders",
        "Shipping",
        "Coupons",
        "Reviews",
    ],
    "Inventory Staff": [
        "Overview",
        "Inventory",
    ],
    "Blog Staff": [
        "Overview",
        "Blog",
    ],
    "Email Support": [
        "Overview",
        "Email Support",
    ],
    "SEO Staff": [
        "Overview",
        "SEO",
        "Blog",
    ],
    "Viewer": [
        "Overview",
    ],
}
