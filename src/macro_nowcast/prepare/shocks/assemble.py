from __future__ import annotations

import pandas as pd

from macro_nowcast.interfaces import Assembler
from macro_nowcast.prepare.shocks import CONTRACT


class ShockAssembler(Assembler):
    domain="shocks"

    def assemble(self, frames: list[pd.DataFrame]) -> pd.DataFrame:
        merged=pd.concat(frames, ignore_index=True)
        return CONTRACT.validate(merged)