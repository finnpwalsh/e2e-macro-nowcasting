import pandas as pd
from pathlib import Path

from src.config.fred import FRED_SERIES
from src.config.fred import FRED_REQUIRED_COLS as REQUIRED_COLS

def test_fred_raw():
    """
    Validate schema and data integrity for raw FRED parquet file.

    Guarantees:
    - columns: date, value, series_id
    - no nulls
    - types (respectively): datetime, float, string
    """
    # read combined series
    df = pd.read_parquet(Path("data/raw") / "fred_all.parquet")

    # check missing columns
    missing_cols = [c for c in REQUIRED_COLS if c not in df.columns]
    assert not missing_cols, f"Missing required columns: {missing_cols}"
    
    # check missing  or extra tickers
    expected = set(FRED_SERIES)
    actual = set(df["ticker"].unique())

    missing_tickers = expected - actual
    extra_tickers = actual - expected
    
    assert not missing_tickers, f"Raw FRED file missing series: {sorted(missing_tickers)}."
    assert not extra_tickers, f"Raw FRED file has unexpected series: {sorted(extra_tickers)}."