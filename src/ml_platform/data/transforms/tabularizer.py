from __future__ import annotations

from typing import Protocol
import pandas as pd


class Tabularizer(Protocol):
    """
    Transforms canonical data into tabular data.
    """
    def tabularize(self, canonical: pd.DataFrame) -> pd.DataFrame:
        ...