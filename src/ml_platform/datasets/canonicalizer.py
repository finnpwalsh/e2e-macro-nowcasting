from __future__ import annotations

from typing import Generic, Protocol, TypeVar

import pandas as pd


D = TypeVar("D")


class Canonicalizer(Protocol, Generic[D]):
    """
    Domain canonicalization step: raw -> canonical.
    """
    domain: D

    def canonicalize(self, raw: pd.DataFrame) -> pd.DataFrame:
        ...