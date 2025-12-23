"""
Cleaning and feature-prep for FRED time-series data.

This module takes raw long-form FRED observations and produces:
- a cleaned long-form dataset (validated, type-enforced, deduped)
- a wide-form dataset for modeling

Input schema (long-form):
    - date (datetime)
    - value (float)
    - series_id (str)

Output:
    - df_long: clean long-form FRED data
    - df_wide: pivoted wide-form data

Called by scripts/clean_fred.py.
"""

from __future__ import annotations
import pandas as pd

REQUIRED_COLS = ["date", "value", "series_id"]

def prep_fred(df_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Orchestrates cleaning and transformation of raw FRED data.

    Returns both a cleaned long-form dataset and a wide-form dataset
    (pivoted from the long-form) for modeling.

    Args:
        df_raw (pd.DataFrame): raw long-form FRED dataset
    
    Returns:
        pd.DataFrame: clean long-form FRED dataset
        pd.DataFrame: clean wide-form FRED dataset (modeling)
    """
    df_long = clean_fred_long(df_raw)
    df_wide = build_fred_wide(df_long)
    return df_long, df_wide

def clean_fred_long(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Dedupes, drops NaNs, coerces dtypes, and sorts for raw long-form
    FRED dataset.

    Args:
        df_raw (pd.DataFrame): raw long-form FRED dataset
    
    Returns:
        pd.DataFrame: long-form clean FRED dataset
    
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

def build_fred_wide(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    Pivots clean long-form FRED data to wide form indexed by date.
    
    Args:
        df_long (pd.DataFrame): clean long-form FRED dataset
    
    Returns:
        pd.DataFrame: clean wide-form FRED dataset
    """
    return (
        df_long.pivot(index="date", columns="series_id", values="value")
        .sort_index()
        .reset_index()
    )