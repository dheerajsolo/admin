from __future__ import annotations

from services.demo_data import get_demo_orders, get_demo_products, get_demo_sales_series, get_demo_shipments


def fetch_orders(limit: int = 50) -> list[dict]:
    return get_demo_orders(limit)


def fetch_products() -> list[dict]:
    return get_demo_products()


def fetch_sales_series(days: int = 14) -> list[dict]:
    return get_demo_sales_series(days)


def fetch_shipments() -> list[dict]:
    return get_demo_shipments()
