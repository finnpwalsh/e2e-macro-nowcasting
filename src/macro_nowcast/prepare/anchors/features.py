from __future__ import annotations

import pandas as pd

from macro_nowcast.interfaces import FeatureBuilder


class AnchorFeatureBuilder(FeatureBuilder):
    domain = "anchors"

    def build(self, canonical: pd.DataFrame) -> pd.DataFrame:
        df = canonical.copy()
        
        df = df.drop(columns=["source"], errors="ignore")

        df["ds"] = (
            pd.to_datetime(df["ds"], errors="raise")
            .dt.tz_localize(None)
            .dt.to_period("M")
            .dt.to_timestamp(how="start") # MS
        )

        df = (
            df.sort_values(["series", "ds"])
            .groupby(["series", "ds"], as_index=False)["value"]
            .last()
        )

        wide = (
            df.pivot(index="ds", columns="series", values="value")
            .sort_index()
            .reset_index()
        )
        
        return wide