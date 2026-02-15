from __future__ import annotations

import pandas as pd
from macro_nowcast.externals.clients.fred import FREDClient


class FREDProvider:
    name = "fred"
    domain = "anchors"

    def __init__(self, client: FREDClient):
        self._client = client

    def fetch(
            self,
            *,
            series: dict[str, str],
            start_date: str,
    ) -> pd.DataFrame:
        """
        Fetch all requested series from FRED and return one raw dataframe.
        """
        dfs: list[pd.DataFrame] = []

        for series_name, series_id in series.items():
            df = self._client.fetch_series(
                series_id=series_id,
                start_date=start_date,
            )

            if df is None or df.empty:
                continue
            
            df = df.copy()
            df["series"] = series_name
            df["series_id"] = series_id
            dfs.append(df)
        
        if not dfs:
            return pd.DataFrame()
        
        out = pd.concat(dfs, ignore_index=True)
        return out.drop_duplicates(subset=["series_id", "date"], keep="last") 