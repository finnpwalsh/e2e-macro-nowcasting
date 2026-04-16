from __future__ import annotations

import pandas as pd

from ml_platform.data.transforms import Canonicalizer


class FREDAnchorCanonicalizer(Canonicalizer):
    """
    Raw FRED -> AnchorLong canonical.
    Expects raw columns: date, value, series, series_id
    Produces: ds, value, series, series_id, source
    """
    name = "fred"

    def canonicalize(self, raw: pd.DataFrame) -> pd.DataFrame:
        out = raw.copy()
        out = out.rename(columns={"date":"ds"})
        out["source"] = self.name

        return out[["ds", "value", "series", "series_id", "source"]]