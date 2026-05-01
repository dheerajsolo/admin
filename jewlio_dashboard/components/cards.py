from __future__ import annotations

from textwrap import dedent


def metric_card(title: str, value: str, note: str, trend: str = "", warn: bool = False) -> str:
    trend_class = "metric-warn" if warn else "metric-good"
    trend_html = f'<span class="{trend_class}">{trend}</span> ' if trend else ""
    return dedent(
        f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{trend_html}{note}</div>
            <div class="sparkline"></div>
        </div>
        """
    )
