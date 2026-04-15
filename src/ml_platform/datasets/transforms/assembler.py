from __future__ import annotations

from typing import Generic, Protocol, TypeVar

import pandas as pd


D = TypeVar("D")


class Assembler(Protocol, Generic[D]):
    """
    Generic dataset assembly step.

    Combines multiple frames that already belong to the same
    logical domain into an assembled dataset.
    """
    domain: D

    def assemble(self, frames: list[pd.DataFrame]) -> pd.DataFrame:
        ...