"""
Make yfinance data merge-ready.

This module takes in a daily long-form yfinance DataFrame and 
outputs a monthly wide-form DataFrame ready for merging with FRED.

INPUT SCHEMA (DataFrame):
- date (datetime)
- value (numeric)
- ticker (string)

OUTPUT:
Monthly wide-form DataFrame
"""
from __future__ import annotations
import pandas as pd

def build_and_resample_yf(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    Thin wrapper function.
    """
    df_wide_daily = build_yf_wide(df_long)
    df_wide_monthly = make_yf_monthly_features(df_wide_daily)
    return df_wide_monthly

def build_yf_wide(df_long: pd.DataFrame) -> pd.DataFrame:
    return df_long.pivot_table(
        index="date", 
        columns="ticker", 
        values="value",
        aggfunc="last" # handle dupes
    ).sort_index()

def make_yf_monthly_features(df_wide_daily: pd.DataFrame) -> pd.DataFrame:
    return (
        df_wide_daily
        .sort_index()
        .resample("MS")
        .last()
    )