from __future__ import annotations
import pandas as pd

def build_merged(
        fred: pd.DataFrame,
        yf: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge FRED and yfinance.
    """
    return (
        fred.merge(yf, on="date", how="inner")
        .sort_values("date")
        .reset_index(drop=True)
    )