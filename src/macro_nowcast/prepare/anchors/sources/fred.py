"""
FRED anchors domain adapter.

Responsibilities:
    - Use FREDClient to fetch raw external data
    - Canonicalize into AnchorLong format
    - Validate against anchors contract
"""
from __future__ import annotations

import pandas as pd

from macro_nowcast.connectors import FREDClient
from macro_nowcast.prepare import Source
from macro_nowcast.prepare.anchors import validate_anchor_long


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
            series_id: str,
            start_date: str,
            **_
    ) -> pd.DataFrame:
        """
        Fetch raw data from FRED via client.
        
        Return minimal DataFrame:
            date, value
        """
        return self._client.fetch_series(
            series_id=series_id,
            start_date=start_date,
        )
    
    def canonicalize(
            self,
            df: pd.DataFrame,
            *,
            series_id: str,
            **_
    ) -> pd.DataFrame:
        """
        Convert raw FRED output into AnchorLong format:
            ds, value, series_id, source
        """
        out = df.copy()

        out = out.rename(columns = {"date":"ds"})

        out["series_id"] = series_id
        out["source"] = self.name

        out["ds"] = pd.to_datetime(out["ds"], errors="coerce").dt.normalize()
        out["value"] = pd.to_numeric(out["value"], errors="coerce")
        out["series_id"] = out["series_id"].astype("string")
        out["source"] = out["source"].astype("string")

        return out[["ds", "value", "series_id", "source"]]
    
    def validate(
            self,
            df: pd.DataFrame,
            **_
    ) -> pd.DataFrame:
        """
        Enforce anchors dataset contract.
        """