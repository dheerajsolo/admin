from __future__ import annotations

from config import settings


def get_data_adapter():
    if settings.api_provider == "woocommerce":
        from adapters import woocommerce_adapter
        return woocommerce_adapter

    from adapters import demo_adapter
    return demo_adapter
