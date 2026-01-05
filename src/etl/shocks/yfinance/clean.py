from __future__ import annotations
import pandas as pd

from .schema import YF_RAW_SCHEMA_COLS as REQUIRED_COLS

def clean_yf_long(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean yfinance long-form data.

    Performs schema validation, data-type coercion, drop invalid rows, 
    dedupes observations (keeps last), and sorts the data.

    Args:
    - df_raw (pd.DataFrame): raw long-form yfinance data

    Returns:
        pd.DataFrame: cleaned long-form data which:
            - has enforced dtypes (datetime, numeric, string)
            - contains no missing values in any column
            - is deduped on (ticker, date) (keeps last)
            - is sorted on ticker then date
    
    Raises:
        ValueError: if raw or cleaned DataFrame is empty
    """
    if df_raw.empty:
        raise ValueError(f"YF long DataFrame (raw) is empty.")
    
    # enforce only required cols exist
    df = df_raw[REQUIRED_COLS].copy()

    # coerce types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors = "coerce")
    df["ticker"] = df["ticker"].astype("string")

    # handle NaNs (DROP in v1)
    df = df.dropna(subset=["date", "value", "ticker"])

    if df.empty:
        raise ValueError("All rows dropped after type coersion and NaN drop.")
    
    # dedupe, sort
    df = df.sort_values(["ticker", "date"])
    df = df.drop_duplicates(subset=["ticker", "date"], keep="last")
    df = df.reset_index(drop=True)

    return df