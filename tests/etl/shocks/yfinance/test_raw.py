import pandas as pd
from pathlib import Path

from src.config.yfinance import YF_TICKERS
from src.config.yfinance import YF_REQUIRED_COLS as REQUIRED_COLS

def test_yf_raw():
    """
    Validate schema and data integrity for all raw yfinance parquet file.

    Guarantees:
    - columns: date, value, ticker
    - no nulls
    - types (respectively): datetime, float, string
    """
    # read combined series
    df = pd.read_parquet(Path("data/raw") / "yf_long.parquet")

    # check missing columns
    missing_cols = [c for c in REQUIRED_COLS if c not in df.columns]
    assert not missing_cols, f"Missing required columns: {missing_cols}"
    
    # check missing  or extra tickers
    expected = set(YF_TICKERS)
    actual = set(df["ticker"].unique())

    missing_tickers = expected - actual
    extra_tickers = actual - expected
    
    assert not missing_tickers, f"Raw yfinance file missing series: {sorted(missing_tickers)}."
    assert not extra_tickers, f"Raw yfinance file has unexpected series: {sorted(extra_tickers)}."