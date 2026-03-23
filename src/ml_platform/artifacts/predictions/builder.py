from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from .schema import Predictions


@dataclass(frozen=True)
class PredictionsBuilder:
    time_col: str
    target_col: str

    def build(
            self,
            *,
            df: pd.DataFrame,
            y_hat,
    ) -> Predictions:
        out = df[[self.time_col, self.target_col]].copy()
        out["y_hat"] = y_hat

        return Predictions(
            df=out,
            time_col=self.time_col,
            target_col=self.target_col,
        )