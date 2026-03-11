from __future__ import annotations

from typing import Protocol
import pandas as pd


class Provider(Protocol):
    """
    Upstream data provider adapter.
    
    Contract:
        - fetch returns RAW provider-shaped data
        - no domain semantics, no validation against domain contracts
    """
    name: str
    domain: str # "anchors" | "shocks"

    def fetch(self, **kwargs) -> pd.DataFrame:
        ...