from __future__ import annotations
import pandas as pd

def build_fred_wide(df: pd.DataFrame) -> pd.DataFrame:
    """
    pivot() assumes df is cleaned long-form FRED data with no (series_id, date) dupes
    """
    if df.empty:
        raise ValueError(f"FRED long dataframe (clean) is empty.")
    
    return df.pivot(index="date", columns="series_id", values="value").sort_index()