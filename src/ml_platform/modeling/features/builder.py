from __future__ import annotations

from typing import Generic, Protocol, TypeVar
import pandas as pd


D = TypeVar("D")


class FeatureBuilder(Protocol, Generic[D]):
    """
    Transforms canonical data into feature-ready data for a given domain.
    """
    domain: D

    def build(self, canonical: pd.DataFrame) -> pd.DataFrame:
        ...