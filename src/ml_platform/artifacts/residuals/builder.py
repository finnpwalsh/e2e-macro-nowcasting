from __future__ import annotations

from dataclasses import dataclass

from ml_platform.artifacts.predictions import Predictions

from .schema import Residuals


@dataclass(frozen=True)
class ResidualsBuilder:
    def build(
            self,
            *,
            predictions: Predictions,
    ) -> Residuals:
        out = predictions.df[[predictions.time_col, predictions.target_col, "y_hat"]].copy()
        out = out.rename(columns={predictions.target_col: "y"})

        return Residuals(
            df=out,
            time_col=predictions.time_col,
        )