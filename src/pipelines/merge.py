from __future__ import annotations
import pandas as pd

from src.utils.time import to_month_index

def build_merged(
        fred: pd.DataFrame,
        yf: pd.DataFrame,
) -> pd.DataFrame:
    fred = to_month_index(fred)
    yf = to_month_index(yf)
    return fred.join(yf, how="inner").sort_index()