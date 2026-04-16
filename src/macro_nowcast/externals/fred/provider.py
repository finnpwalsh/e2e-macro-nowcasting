from __future__ import annotations

import pandas as pd

from .client import FREDClient


class FREDProvider:
    name = "fred"

    def __init__(
        self,
        *,
        client: FREDClient,
    ) -> None:
        self._client = client

    def fetch(
            self,
            *,
            series: dict[str, str],
            start_date: str,
            end_date: str | None = None,
    ) -> pd.DataFrame:
        """
        Fetch all requested series from FRED and return one raw dataframe.
        """
        dfs: list[pd.DataFrame] = []

        for series_name, series_id in series.items():
            df = self._client.fetch(
                series_id=series_id,
                start_date=start_date,
                end_date=end_date,
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