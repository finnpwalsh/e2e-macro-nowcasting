from __future__ import annotations

from typing import Generic, Protocol, TypeVar

import pandas as pd


D = TypeVar("D")


class Provider(Protocol, Generic[D]):
    """
    Upstream data provider adapter.
    
    Contract:
        - fetch returns raw provider-shaped data
        - no domain semantics beyond domain identity
        - no validation against downstream domain contracts
    """
    name: str
    domain: D

    def fetch(self, **kwargs) -> pd.DataFrame:
        ...