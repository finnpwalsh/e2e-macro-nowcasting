from __future__ import annotations

from typing import Protocol

import pandas as pd


class Canonicalizer(Protocol):
    """
    Canonicalization step: raw -> canonical.
    """

    def canonicalize(self, raw: pd.DataFrame) -> pd.DataFrame:
        ...