"""
Ingest raw yfinance data and output raw DataFrame with
minimal schema enforcement.

RESPONSIBILITIES:
- Ingest raw yfinance data as DataFrame
- Add ticker column to DataFrame
- Assert minimal schema

OUTPUT:
Raw DataFrame with minimal schema enforcement.
"""
from __future__ import annotations

import pandas as pd
import yfinance as yf

from src.config.yfinance import YF_REQUIRED_COLS as REQUIRED_COLS

START_DATE = "2010-01-01"

def assert_yf_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    ASSERTS:
    - df is not empty
    - all required columns exist
    - date and value are not all null
    - ticker is not null
    """
    if df.empty:
        raise ValueError("YF DataFrame is empty.")

    # assert required cols exist
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"YF DataFrame missing column(s): {missing}")

    # assert non NaNs
    if df["date"].isna().sum() == len(df):
        raise ValueError(f"All dates are NaN.")
    if df["value"].isna().sum() == len(df):
        raise ValueError(f"All values are NaN")
    if df["ticker"].isna().any():
        raise ValueError(f"Missing {df['ticker'].isna().sum()} tickers.")
    
    # else, valid data frame
    return df


def ingest_yf_series(
        ticker: str,
        start: str = START_DATE,
) -> pd.DataFrame:
    t = yf.download(ticker, start=start, progress=False)

    # check null download
    if t is None or t.empty:
        raise ValueError(f"{ticker}: yfinance returned no data (start={start}).")
    
    # choose one price col
    col = "Adj Close" if "Adj Close" in t.columns else "Close"

    # make df from series
    df = t[[col]].rename(columns={col: "value"}).reset_index()
    df.columns = ["date", "value"]

    # assign ticker to new col
    df["ticker"] = ticker

    df = assert_yf_schema(df)
    return df
