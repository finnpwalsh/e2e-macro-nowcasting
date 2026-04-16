from __future__ import annotations

import pandas as pd

from ml_platform.data.transforms import Canonicalizer

class TiingoShockCanonicalizer(Canonicalizer):
    """
    Raw Tiingo -> ShockLong canonical.
    Expects raw columns: date, value, ticker, ticker_id
    Produces: ts, value, ticker, ticker_id, source
    """

    def canonicalize(self, raw: pd.DataFrame):
        out = raw.copy()
        out = out.rename(columns={"date":"ts"})
        out["source"] = "tiingo"

        return out[["ts", "value", "ticker", "ticker_id", "source"]]