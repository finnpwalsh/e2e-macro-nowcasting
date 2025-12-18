import pandas as pd
from pathlib import Path

REQUIRED_COLS = ["value", "date", "series_id"]

def test_fred_raw_contract():
    """
    Finds all raw FRED files and ensures they follow schema.

    Guarantees:
    - columns: date, value, series_id
    - no nulls
    - types (respectively): datetime, float, string

    Future changes:
    - define an explicit fred series list and enforce
        + keep a list in .env or config file and have test
        + iterate through list
    """

    # check in-file paths
    files = sorted(Path("data/raw").glob("fred_*.parquet"))
    assert files, f"No FRED raw parquet files found in data/raw"
    
    for infile in files:
        # read parquet
        df = pd.read_parquet(infile)

        # check missing columns
        missing = set(REQUIRED_COLS) - set(df.columns)
        assert not missing, f"Missing required columns: {sorted(missing)}"

        # check null values
        nn_cols = ["date", "series_id"]
        assert not df[nn_cols].isna().any().any()
        assert not df["value"].isna().sum() == len(df)

        # check valid data types
        assert pd.api.types.is_float_dtype(df["value"]), f"Expected float type, got {df['value'].dtype}"
        assert pd.api.types.is_datetime64_any_dtype(df["date"]), f"Expected datetime type, got {df['date'].dtype}"
        assert pd.api.types.is_string_dtype(df["series_id"]), f"Expected string type, got {df['series_id'].dtype}"
    
