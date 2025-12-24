from __future__ import annotations

import pandas as pd

from src.pipelines.fred import clean_fred_long
from src.config.fred import FRED_REQUIRED_COLS as REQUIRED_COLS

def test_fred_clean():
    # bad df for testing
    df_in = pd.DataFrame(
        {
        "date" : ["2020-01-01", "2020-01-01", "baddate", None],
        "series_id" : ["CPIAUCSL", "CPIAUCSL", "CPIAUCSL", "CPIAUCSL"],
        "value" : ["1.0", "2.0", "3.0", None],
        }
    )

    # clean
    df = clean_fred_long(df_in)

    # check df exists
    assert not df.empty, "test df empty after cleaning."

    # check df has all required cols
    assert all(c in df.columns for c in REQUIRED_COLS), "test df missing 1+ columns after cleaning."

    # check nulls
    assert df[REQUIRED_COLS].notna().all().all(), "test df has nulls after cleaning."

    # check types
    assert pd.api.types.is_datetime64_any_dtype(df["date"]), f"test df date not datetime type: {df['date'].dtype} after cleaning."
    assert pd.api.types.is_numeric_dtype(df["value"]), f"test df value not numeric type: {df['value'].dtype} after cleaning."
    assert pd.api.types.is_string_dtype(df["series_id"]), f"test df series id not string type: {df['series_id'].dtype} after cleaning."

    # check for dupes
    assert not df.duplicated(subset=["series_id", "date"]).any(), "test df has dupes after cleaning."
    
    # check df has 1 row (3 rows removed)
    assert len(df) == 1, f"test df has {len(df)-1} more rows than expected after cleaning."