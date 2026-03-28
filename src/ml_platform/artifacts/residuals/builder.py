from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from ml_platform.artifacts.predictions import Predictions

from .schema import Residuals


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