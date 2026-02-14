"""
Anchors dataset contracts.

Defines the canonical formats for anchors-domain data.
"""
from __future__ import annotations

from typing import Tuple

import pandas as pd

from macro_nowcast.prepare.interfaces import Contract


class AnchorContract(Contract):
    """
    Canonical anchors contract.
    """

    @property
    def columns(self) -> Tuple[str, ...]:
        return (
            "ds",
            "value",
            "series",
            "series_id",
            "source",
        )
    
    @property
    def primary_key(self) -> Tuple[str, ...]:
        return (
            "source",
            "series",
            "ds",
        )
    

    def coerce(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)
        df["value"] = pd.to_numeric(df["value"], errors="raise")

        df["series"] = df["series"].astype(str)
        df["series_id"] = df["series_id"].astype(str)
        df["source"] = df["source"].astype(str)

        df = df.sort_values(list(self.primary_key)).reset_index(drop=True)

        return df


CONTRACT = AnchorContract()