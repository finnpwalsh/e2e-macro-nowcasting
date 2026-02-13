"""
FRED anchors domain adapter.

Responsibilities:
    - Use FREDClient to fetch raw external data
    - Canonicalize into AnchorLong format
    - Validate against anchors contract
"""
from __future__ import annotations

import pandas as pd

from macro_nowcast.prepare import Source
from macro_nowcast.prepare.anchors import CONTRACT
from .client import FREDClient


class FREDSource(Source):
    """
    Anchors-domain adapter for FRED.
    """

    name = "fred"
    domain = "anchors"

    def __init__(self, client: FREDClient):
        self._client = client

    def fetch(
            self,
            *,
            series: dict[str, str],
            start_date: str,
            **_
    ) -> pd.DataFrame:
        """
        Fetch all requested series from FRED and return one raw dataframe.

        Raw columns:
            date, value, series, series_id, 
        """
        dfs: list[pd.DataFrame] = []

        for series_name, series_id in series.items():
            df = self._client.fetch_series(
                series_id=series_id,
                start_date=start_date,
            )
            df = df.copy()
            df["series"] = series_name
            df["series_id"] = series_id
            dfs.append(df)
        
        return pd.concat(dfs, ignore_index=True)
    
    def canonicalize(
            self,
            df: pd.DataFrame,
            *,
            series: dict[str, str],
            **_
    ) -> pd.DataFrame:
        """
        Convert raw FRED output into AnchorLong format:
            ds, value, series_id, source
        """
        out = df.copy()

        out = out.rename(columns = {"date":"ds"})
        out["source"] = self.name

        return out[["ds", "value", "series", "series_id", "source"]]
    
    def validate(
            self,
            df: pd.DataFrame,
            **_
    ) -> pd.DataFrame:
        """
        Enforce anchors dataset contract.
        """
        return CONTRACT.validate(df)