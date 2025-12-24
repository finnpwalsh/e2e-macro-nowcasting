import pandas as pd
from pathlib import Path

from src.config.fred import FRED_SERIES
from src.config.fred import FRED_REQUIRED_COLS as REQUIRED_COLS

def test_fred_raw():
    """
    Validate schema and data integrity for all raw FRED parquet files.

    Guarantees:
    - columns: date, value, series_id
    - no nulls
    - types (respectively): datetime, float, string
    """

    # check in-file paths, excluding combined file
    files = sorted(Path("data/raw").glob("fred_*.parquet"))
    files = [p for p in files if p.name != "fred_all.parquet"]
    assert files, f"No individual FRED raw parquet files found in data/raw"
    
    for infile in files:
        # read parquet
        df = pd.read_parquet(infile)

        # check missing columns
        missing = set(REQUIRED_COLS) - set(df.columns)
        assert not missing, f"Missing required columns: {sorted(missing)}"

        # check null values
        nn_cols = ["date", "series_id"]
        assert not df[nn_cols].isna().any().any(), f"Nulls found in {infile.name} for {nn_cols}."
        assert not df["value"].isna().sum() == len(df), f"All values in {infile.name} are null."

        # check valid data types
        assert pd.api.types.is_float_dtype(df["value"]), f"Expected float type, got {df['value'].dtype}"
        assert pd.api.types.is_datetime64_any_dtype(df["date"]), f"Expected datetime type, got {df['date'].dtype}"
        assert pd.api.types.is_string_dtype(df["series_id"]), f"Expected string type, got {df['series_id'].dtype}"

    # read combined series
    combined = pd.read_parquet(Path("data/raw") / "fred_all.parquet")
    
    # check missing  or extra series in combined
    expected = set(FRED_SERIES)
    actual = set(combined["series_id"].unique())

    missing = expected - actual
    extra = actual - expected
    
    assert not missing, f"Combined FRED file missing series: {sorted(missing)}."
    assert not extra, f"Combined FRED file has unexpected series: {sorted(extra)}."