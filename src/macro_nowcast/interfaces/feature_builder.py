from __future__ import annotations

from typing import Protocol, Literal
import pandas as pd

Domain = Literal["anchors", "shocks"]


class FeatureBuilder(Protocol):
    domain: Domain

    def build(self, canonical: pd.DataFrame) -> pd.DataFrame:
        ...