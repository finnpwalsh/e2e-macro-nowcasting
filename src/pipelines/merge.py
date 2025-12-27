from __future__ import annotations
import pandas as pd

def build_merged(
        fred: pd.DataFrame,
        yf: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge FRED and yfinance.
    """
    return fred.join(yf, how="inner").sort_index()