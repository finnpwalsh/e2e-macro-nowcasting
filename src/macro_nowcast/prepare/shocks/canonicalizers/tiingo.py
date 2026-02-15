from __future__ import annotations

import pandas as pd
from .base import ShockCanonicalizer


class TiingoShockCanonicalizer(ShockCanonicalizer):
    """
    Raw Tiingo -> ShockLong canonical.
    Expects raw columns: date, value, ticker, ticker_id
    Produces: ts, value, ticker, ticker_id, source
    """
    name="tiingo"

    def canonicalize(self, raw: pd.DataFrame):
        out = raw.copy()
        out = out.rename(columns={"date":"ts"})
        out["source"] = self.name

        return out[["ds", "value", "ticker", "ticker_id", "source"]]