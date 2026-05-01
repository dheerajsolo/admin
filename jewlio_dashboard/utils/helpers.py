from __future__ import annotations

import pandas as pd


def find_col(df: pd.DataFrame, possible_names: list[str]) -> str | None:
    for name in possible_names:
        if name in df.columns:
            return name
    return None
