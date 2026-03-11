from __future__ import annotations

import pandas as pd
from macro_nowcast.prepare._interfaces import FeatureBuilder


class ShockFeatureBuilder(FeatureBuilder):
    domain="shocks"

    def build(self, canonical: pd.DataFrame) -> pd.DataFrame:
        df = canonical.copy()
        
        df = df.drop(columns=["source"], errors="ignore")

        df["ts"] = (
            pd.to_datetime(df["ts"], errors="raise")
            .dt.tz_localize(None)
            .dt.floor("D")
        )

        df = (
            df.sort_values(["ticker", "ts"])
            .groupby(["ticker", "ts"], as_index=False)["value"]
            .last()
        )

        wide = (
            df.pivot(index="ts", columns="ticker", values="value")
            .sort_index()
            .reset_index()
        )
        
        return wide