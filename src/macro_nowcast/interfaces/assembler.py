from __future__ import annotations

from typing import Protocol, Literal
import pandas as pd

Domain = Literal["anchors", "shocks"]


class Assembler(Protocol):
    domain: Domain

    def assemble(self, frames: list[pd.DataFrame]) -> pd.DataFrame:
        ...
