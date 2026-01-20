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
    - df_long (pd.DataFrame): clean long-form FRED data
    - df_wide (pd.DataFrame): pivoted wide-form data

Called by scripts/clean_fred.py.
"""
from __future__ import annotations
import pandas as pd

from .clean import clean_fred_long
from .build_wide import build_fred_wide

def prep_fred(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Orchestrates cleaning and transformation of raw FRED data.

    Returns both a cleaned long-form dataset and a wide-form dataset
    (pivoted from the long-form) for modeling.

    Args:
        df_raw (pd.DataFrame): raw long-form FRED dataset
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]:
            df_long: clean long-form FRED dataset
            df_wide: clean wide-form FRED dataset (modeling)
    """
    df_long = clean_fred_long(df_raw)
    df_wide = build_fred_wide(df_long)
    return df_wide

