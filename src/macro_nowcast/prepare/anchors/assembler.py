from __future__ import annotations

import pandas as pd

from .contract import CONTRACT

from ml_platform.data.transforms import Assembler


class AnchorAssembler(Assembler):
    domain = "anchors"

    def assemble(self, frames: list[pd.DataFrame]) -> pd.DataFrame:
        merged = pd.concat(frames, ignore_index=True)
        return CONTRACT.validate(merged)