from __future__ import annotations
import pandas as pd

from .clean import clean_yf_long
from .build_monthly import build_and_resample_yf

def prep_yf(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Orchestrates yfinance cleaning and pivoting.
    """
    df_long = clean_yf_long(df_raw)
    df_wide = build_and_resample_yf(df_long)
    return df_wide