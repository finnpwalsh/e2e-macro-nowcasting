from __future__ import annotations
import pandas as pd

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
        .resample("M")
        .last()
    )