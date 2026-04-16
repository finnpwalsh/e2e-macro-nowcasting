from __future__ import annotations

import pandas as pd

from ml_platform.data.transforms import Assembler
from .contract import CONTRACT


class ShockAssembler(Assembler):
    def assemble(self, frames: list[pd.DataFrame]) -> pd.DataFrame:
        merged=pd.concat(frames, ignore_index=True)
        return CONTRACT.validate(merged)