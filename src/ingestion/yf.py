from __future__ import annotations

import pandas as pd
import yfinance as yf

from src.config.yf import YF_TICKERS, YF_REQUIRED_COLS

START_DATE = "2010-01-01"

def validate_yf(df: pd.DataFrame) -> pd.DataFrame:
    # check required cols exist
    missing = [c for c in YF_REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"yf DataFrame missing column(s): {missing}")
    
    # coerce types
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.normalize()
    df["value"] = pd.to_numeric(df["value"], errors = "coerce")
    df["ticker"] = df["ticker"].astype("string")

    # date and series_id must be valid, must have at least 1 valid value
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

    df = validate_yf(df)
    return df
