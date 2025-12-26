"""
FRED raw data ingestion and validation.

RESPONSIBILITIES:
- Fetch series from FRED
- Enforce raw data schema
- Write validated data to raw parquet

OUTPUT:
Raw FRED DataFrame
"""
from __future__ import annotations

import pandas as pd
from fredapi import Fred

from src.config.fred import FRED_REQUIRED_COLS as REQUIRED_COLS

def validate_fred(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Make sure...
    - Required columns exist
        + date, value, series_id
    - no null values
    - variables coerced to schema:
        + date        datetime64[ns]
        + value       float64
        + series_id   string
    '''
    
    # check required cols exist
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # coerce types
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.normalize()
    df["value"] = pd.to_numeric(df["value"], errors = "coerce")
    df["series_id"] = df["series_id"].astype("string")

    # date and series_id must be valid, must have at least 1 valid value
    if df["date"].isna().any():
        raise ValueError(f"Missing {df['date'].isna().sum} dates.")
    if df["series_id"].isna().any():
        raise ValueError(f"Missing {df['series_id'].isna().sum} series IDs.")
    if df["value"].isna().sum() == len(df):
        raise ValueError(f"All values are NaN")
    
    # else, valid data frame
    return df


def ingest_fred_series(
    fred: Fred, 
    series_id: str,
    start: str = "2010-01-01",
) -> pd.DataFrame:
    '''
    Ingest FRED api and return coerced + validated raw data.
    
    :param fred: FRED api
        :type fred: Fred
    :param series_id: FRED series id
        :type series_id: str
    :param start: start date
        :type start: str
    :return: validated raw FRED data
        :rtype: DataFrame
    '''
    # ingest
    s = fred.get_series(series_id, observation_start = start)

    # if null raise error
    if s is None or len(s) == 0:
        raise RuntimeError(f"No data returned for series_id={series_id}")
    
    # series -> data frame
    df = s.to_frame(name="value").reset_index()
    df.columns = ["date", "value"]
    
    # assign series id to new column
    df["series_id"] = series_id

    # validate and return
    df = validate_fred(df)
    return df