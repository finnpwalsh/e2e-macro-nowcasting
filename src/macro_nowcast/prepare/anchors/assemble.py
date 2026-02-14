from __future__ import annotations

import pandas as pd

from macro_nowcast.interfaces.assembler import Assembler
from macro_nowcast.prepare.anchors.contract import CONTRACT


class AnchorAssembler(Assembler):
    domain = "anchors"

    def assemble(self, frames: list[pd.DataFrame]) -> pd.DataFrame:
        merged = pd.concat(frames, ignore_index=True)
        return CONTRACT.validate(merged)