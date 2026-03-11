from __future__ import annotations

import pandas as pd

from macro_nowcast.prepare._interfaces import Assembler
from .contract import CONTRACT


class AnchorAssembler(Assembler):
    domain = "anchors"

    def assemble(self, frames: list[pd.DataFrame]) -> pd.DataFrame:
        merged = pd.concat(frames, ignore_index=True)
        return CONTRACT.validate(merged)