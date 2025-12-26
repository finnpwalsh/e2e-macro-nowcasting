from __future__ import annotations
import pandas as pd

def to_month_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize a DatetimeIndex to month-end timestamps.
    """
    out = df.copy()
    out.index = (
        pd.to_datetime(out.index)
        .to_period("M")
        .to_timestamp("M")
    )
    return out