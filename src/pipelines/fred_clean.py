from __future__ import annotations
import pandas as pd

REQUIRED_COLS = ["date", "value", "series_id"]

def clean_fred_long(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError(f"FRED long dataframe (raw) is empty.")
    
    # check required cols exist
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in raw FRED: {missing}")
    
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