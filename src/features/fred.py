from __future__ import annotations
import pandas as pd

def build_fred_wide(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    Pivots clean long-form FRED data to wide form indexed by date.
    
    Args:
        df_long (pd.DataFrame): clean long-form FRED dataset
    
    Returns:
        pd.DataFrame: clean wide-form FRED dataset
    """
    return (
        df_long.pivot(index="date", columns="series_id", values="value")
        .sort_index()
        .reset_index()
    )