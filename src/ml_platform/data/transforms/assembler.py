from __future__ import annotations

from typing import Protocol

import pandas as pd


class Assembler(Protocol):
    """
    Input tables -> assembled dataframe.
    """
    def assemble(self, dfs: tuple[pd.DataFrame, ...]) -> pd.DataFrame:
        ...