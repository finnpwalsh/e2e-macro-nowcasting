from __future__ import annotations

import pandas as pd
from fredapi import Fred


class FREDClient:
    def __init__(self, api_key: str):
        self._fred = Fred(api_key=api_key)
    
    def fetch_series(self, *, series_id: str, start_date: str) -> pd.DataFrame:
        s = self._fred.get_series(series_id, observation_start = start_date)
        return (
            s.rename("value")
             .reset_index()
             .rename(columns = {"index":"date"})
        )