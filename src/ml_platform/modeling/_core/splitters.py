from __future__ import annotations

from typing import Protocol

import pandas as pd


class Splitter(Protocol):
    def split(
        self,
        *,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        ...