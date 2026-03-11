from __future__ import annotations

from typing import Protocol, Literal
import pandas as pd

Domain = Literal["anchors", "shocks"]

class Canonicalizer(Protocol):
    """
    Domain canonicalization step: raw -> canonical.
    """
    domain: Domain

    def canonicalize(self, **kwargs) -> pd.DataFrame:
        ...