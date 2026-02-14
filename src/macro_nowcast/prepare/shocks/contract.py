"""
Shocks dataset contract.

Defines the canonical format for shock-domain data.
"""
from __future__ import annotations

from typing import Tuple

import pandas as pd

from macro_nowcast.prepare.interfaces import Contract


class ShockContract(Contract):
    @property
    def columns(self) -> Tuple[str, ...]:
        return(
            "ts",
            "value",
            "ticker",
            "ticker_id",
            "source",
        )
    
    @property
    def primary_key(self) -> Tuple[str, ...]:
        return (
            "source",
            "series",
            "ts",
        )
    
    def coerce(self, df: pd.DataFrame) -> pd.DataFrame:
        df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)
        df["value"] = pd.to_numeric(df["value"], errors="raise")

        df["ticker"] = df["ticker"].astype(str)
        df["ticker"] = df["ticker"].astype(str)
        df["ticker"] = df["ticker"].astype(str)

        df = df.sort_values(list(self.primary_key)).reset_index(drop=True)

        return df