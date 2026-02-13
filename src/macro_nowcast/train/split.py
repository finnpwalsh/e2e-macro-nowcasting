from __future__ import annotations

import pandas as pd


def time_split_mask(
    df: pd.DataFrame,
    *,
    date_col: str="date",
    split_date: str,
) -> tuple[pd.Series, pd.Series]:
    d = pd.to_datetime(df[date_col])
    cutoff = pd.to_datetime(split_date)
    
    train = d < cutoff
    valid = ~train

    return train, valid