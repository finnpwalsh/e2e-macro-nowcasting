from __future__ import annotations

import pandas as pd

from macro_nowcast.interfaces.feature_builder import FeatureBuilder


class AnchorFeatureBuilder(FeatureBuilder):
    domain = "anchors"

    def build(self, canonical: pd.DataFrame) -> pd.DataFrame:
        wide = (
            canonical
            .pivot(index="ds", columns="series", values="value")
            .sort_index()
            .reset_index()
        )
        return wide