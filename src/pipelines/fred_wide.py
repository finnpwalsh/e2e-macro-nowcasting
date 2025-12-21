from __future__ import annotations
import pandas as pd

def build_fred_wide(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError(f"FRED long dataframe (clean) is empty.")
    
    return df.pivot(index="date", columns="series_id", values="value").sort_index()