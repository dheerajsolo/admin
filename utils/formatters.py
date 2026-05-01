from __future__ import annotations

from datetime import datetime
from typing import Any


def money(value: Any) -> str:
    try:
        return f"₹{float(value):,.0f}"
    except Exception:
        return "₹0"


def number(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except Exception:
        return "0"


def short_date(value: Any) -> str:
    if not value:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y")
    text = str(value).replace("T", " ")
    try:
        return datetime.fromisoformat(text[:19]).strftime("%d %b %Y")
    except Exception:
        return text[:10]


def safe_text(value: Any, fallback: str = "-") -> str:
    if value is None or value == "":
        return fallback
    return str(value)
