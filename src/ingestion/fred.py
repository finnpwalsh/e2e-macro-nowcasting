from __future__ import annotations

import pandas as pd
from fredapi import Fred

def ingest_fred_series(
    fred: Fred, 
    series_id: str,
    start: str = "2010-01-01",
) -> pd.DataFrame:
    
    s = fred.get_series(series_id, observation_start = start)

    if s is None or len(s) == 0:
        raise RuntimeError(f"No data returned for series_id={series_id}")
    
    df = s.to_frame(name="value").reset_index()
    df.columns = ["date", "value"]
    df["series_id"] = series_id
    
    return df