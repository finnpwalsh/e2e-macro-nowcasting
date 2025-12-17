import pandas as pd
from pathlib import Path

REQUIRED_COLS = ["value", "date", "series_id"]

def test_fred_raw_contract():
    # check in-file path
    infile = Path("data/raw") / "fred_CPIAUCSL.parquet"
    assert infile.exists(), f"Missing in-file: {infile}"
    
    # read parquet
    df = pd.read_parquet(infile)

    # check missing columns
    missing = set(REQUIRED_COLS) - set(df.columns)
    assert not missing, f"Missing required columns: {sorted(missing)}"

    # check null values
    assert not df[REQUIRED_COLS].isna().any().any()

    # check valid data types
    assert pd.api.types.is_float_dtype(df["value"]), f"Expected float type, got {df['value'].dtype}"
    assert pd.api.types.is_datetime64_any_dtype(df["date"]), f"Expected datetime type, got {df['date'].dtype}"
    assert pd.api.types.is_string_dtype(df["series_id"]), f"Expected string type, got {df['series_id'].dtype}"