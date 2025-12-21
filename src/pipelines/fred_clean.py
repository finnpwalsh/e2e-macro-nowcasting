from __future__ import annotations
import pandas as pd

REQUIRED_COLS = ["date", "value", "series_id"]

def prep_fred(df_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_long = clean_fred_long(df_raw)
    df_wide = build_fred_wide(df_long)
    return df_long, df_wide

def clean_fred_long(df_raw: pd.DataFrame) -> pd.DataFrame:
    if df_raw.empty:
        raise ValueError(f"FRED long dataframe (raw) is empty.")
    
    # check required cols exist
    missing = [c for c in REQUIRED_COLS if c not in df_raw.columns]
    if missing:
        raise ValueError(f"Missing required columns in raw FRED: {missing}")
    
    df = df_raw.copy()

    # coerce types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors = "coerce")
    df["series_id"] = df["series_id"].astype("string")

    # handle NaNs (DROP in v1)
    df = df.dropna(subset=["date", "value", "series_id"])
    
    # dedupe, sort
    df = df.sort_values(["series_id", "date"])
    df = df.drop_duplicates(subset=["series_id", "date"], keep="last")
    df = df.reset_index(drop=True)

    return df

def build_fred_wide(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    pivot() assumes df is cleaned long-form FRED data with no (series_id, date) dupes
    """
    if df_long.empty:
        raise ValueError("FRED long dataframe (clean) is empty.")
    
    return (
        df_long.pivot(index="date", columns="series_id", values="value")
        .sort_index()
        .reset_index()
    )