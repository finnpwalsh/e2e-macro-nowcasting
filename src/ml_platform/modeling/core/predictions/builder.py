from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .schema import Predictions


@dataclass(frozen=True)
class PredictionsBuilder:
    target: str
    row_id: str | None = None

    def build(
            self,
            *,
            df: pd.DataFrame,
            y_hat: pd.Series,
    ) -> Predictions:
        if len(df) != len(y_hat): raise ValueError(
            f"Length mismatch: df={len(df)}, y_hat={len(y_hat)}"
        )

        out = pd.DataFrame(index=df.index)
        out["y"] = df[self.target].to_numpy()
        out["y_hat"] = pd.Series(y_hat, index=df.index)

        if self.row_id is not None:
            out["row_id"] = df[self.row_id].to_numpy()

        return Predictions(df=out)