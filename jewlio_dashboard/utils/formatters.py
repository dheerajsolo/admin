from __future__ import annotations


def money(value) -> str:
    try:
        return f"Rs. {float(value):,.0f}"
    except Exception:
        return "Rs. 0"


def to_float(value) -> float:
    try:
        if value is None:
            return 0.0
        return float(str(value).replace(",", "").replace("Rs.", "").replace("₹", "").strip())
    except Exception:
        return 0.0


def clean_text(value, fallback: str = "-") -> str:
    text = str(value or "").strip()
    return text if text else fallback
