from __future__ import annotations

from typing import Protocol

import pandas as pd


class Provider(Protocol):
    """
    Upstream data provider adapter.
    """
    name: str

    def fetch(self, **kwargs) -> pd.DataFrame:
        ...