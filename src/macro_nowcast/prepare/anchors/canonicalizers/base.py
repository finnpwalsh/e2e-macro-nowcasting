from __future__ import annotations

import pandas as pd
from macro_nowcast.interfaces.canonicalizer import Canonicalizer


class AnchorCanonicalizer(Canonicalizer):
    domain = "anchors"
    
    def canonicalize(self, raw: pd.DataFrame) -> pd.DataFrame:
        ...