from __future__ import annotations

import pandas as pd

from src.pipelines.yfinance import clean_yf_long
from src.config.yfinance import YF_REQUIRED_COLS as REQUIRED_COLS

def test_yf_clean():
    # bad df for testing
    df_in = pd.DataFrame(
        {
        "date" : ["2020-01-01", "2020-01-01", "baddate", None],
        "value" : ["1.0", "2.0", "3.0", None],
        "ticker" : ["SPY", "SPY", "SPY", "SPY"],
        }
    )

    # clean
    df = clean_yf_long(df_in)

    # check df exists
    assert not df.empty, "test df empty after cleaning."

    # check df has all required cols
    assert all(c in df.columns for c in REQUIRED_COLS), "test df missing 1+ columns after cleaning."

    # check nulls
    assert df[REQUIRED_COLS].notna().all().all(), "test df has nulls after cleaning."

    # check types
    assert pd.api.types.is_datetime64_any_dtype(df["date"]), f"test df date not datetime type: {df['date'].dtype} after cleaning."
    assert pd.api.types.is_numeric_dtype(df["value"]), f"test df value not numeric type: {df['value'].dtype} after cleaning."
    assert pd.api.types.is_string_dtype(df["ticker"]), f"test df ticker not string type: {df['ticker'].dtype} after cleaning."

    # check for dupes
    assert not df.duplicated(subset=["ticker", "date"]).any(), "test df has dupes after cleaning."
    
    # check df has 1 row (3 rows removed)
    assert len(df) == 1, f"test df has {len(df)-1} more rows than expected after cleaning."