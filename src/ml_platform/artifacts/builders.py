from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import pandas as pd

from .schema import Predictions, Residuals


@dataclass(frozen=True)
class PredictionsBuilder:
    target_col: str
    row_id_col: str | None = None

    def build(
            self,
            *,
            df: pd.DataFrame,
            y_hat: Any,
    ) -> Predictions:
        if len(df) != len(y_hat): raise ValueError(
            f"Length mismatch: df={len(df)}, y_hat={len(y_hat)}"
        )

        out = pd.DataFrame(index=df.index)
        out["y"] = df[self.target_col].to_numpy()
        out["y_hat"] = pd.Series(y_hat, index=df.index)

        if self.row_id_col is not None:
            out["row_id"] = df[self.row_id_col].to_numpy()

        return Predictions(df=out)


@dataclass(frozen=True)
class ResidualsBuilder:
    def build(
            self,
            *,
            predictions: Predictions,
    ) -> Residuals:
        out = pd.DataFrame(index=predictions.df.index)
        
        out["y"] = predictions.y
        out["y_hat"] = predictions.y_hat
        out["residual"] = out["y"] - out["y_hat"]

        if predictions.row_id is not None:
            out["row_id"] = predictions.row_id

        return Residuals(df=out)