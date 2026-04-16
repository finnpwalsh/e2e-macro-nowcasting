from __future__ import annotations

from typing import Generic, Protocol, TypeVar

import pandas as pd


D = TypeVar("D")


class Provider(Protocol, Generic[D]):
    """
    Upstream data provider adapter.
    """
    name: str

    def fetch(self, **kwargs) -> pd.DataFrame:
        ...