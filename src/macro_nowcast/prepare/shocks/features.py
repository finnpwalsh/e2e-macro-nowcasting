from __future__ import annotations

import pandas as pd
from macro_nowcast.interfaces import FeatureBuilder


class ShockFeatureBuilder(FeatureBuilder):
    domain="shocks"

    def build(self, canonical: pd.DataFrame) -> pd.DataFrame:
        wide = (
            canonical
            .pivot(index="ts", columns="ticker", values="value")
            .sort_index()
            .reset_index()
        )
        return wide