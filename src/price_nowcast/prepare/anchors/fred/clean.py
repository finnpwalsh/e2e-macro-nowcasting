from __future__ import annotations
import pandas as pd

from .schema import FRED_RAW_SCHEMA_COLS as REQUIRED_COLS

def clean_fred_long(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw long-form FRED data.

    Performs schema validation, coerce dtypes, drops invalid rows,
    dedupes observations, and sorts the data.

    Args:
        df_raw (pd.DataFrame): raw long-form FRED dataset with cols:
            [date, value, series_id]
    
    Returns:
        pd.DataFrame: cleaned long-form FRED dataset which
        - has enforced dtypes (datetime, numeric, string)
            - contains no missing values in date, value, or series_id
            - is deduped on (series_id, date) (keeps last)
            - is sorted by series_id, then date
    
    Raises:
        ValueError: if the input DataFrame is empty or missing required 
                    columns
    """
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

