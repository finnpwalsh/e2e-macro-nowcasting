from __future__ import annotations

import pandas as pd
from fredapi import Fred

REQUIRED_COLS = ["date", "value", "series_id"]

def validate_fred(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Schema:
        date        datetime64[ns]
        value       float64
        series_id   string
    '''
    
    # check required cols exist
    missing = set(REQUIRED_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # coerce
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors = "coerce")
    df["series_id"] = df["series_id"].astype("string")

    # if ANY NaN values exist, raise error w/ count
    bad = df.isna().sum()
    if bad.any():
        raise ValueError(f"Invalid FRED data after type coersion. NaN counts: {bad.to_dict()}")

    # else, valid data frame
    return df

def ingest_fred_series(
    fred: Fred, 
    series_id: str,
    start: str = "2010-01-01",
) -> pd.DataFrame:
    
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