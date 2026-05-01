from __future__ import annotations


def badge(text: str, status: str = "pending") -> str:
    safe_status = str(status or "pending").lower().replace(" ", "-")
    return f"<span class='badge {safe_status}'>{text}</span>"
