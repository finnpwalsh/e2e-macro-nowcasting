from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

from ml_platform.modeling._core import Predictions


@dataclass(frozen=True)
class RegressionMetrics:
    rmse: float
    mae: float
    r2: float
    mape: float | None

    def to_dict(self) -> dict[str, float]:
        out =  {
            "rmse": self.rmse,
            "mae": self.mae,
            "r2": self.r2,
        }
        if self.mape is not None:
            out["mape"] = self.mape
        
        return out


@dataclass(frozen=True)
class RegressionScorer:
    def score(
            self,
            *,
            predictions: Predictions,
    ) -> RegressionMetrics:
        y = np.asarray(predictions.y)
        y_hat = np.asarray(predictions.y_hat)

        rmse = float(np.sqrt(mean_squared_error(y, y_hat)))
        mae = float(mean_absolute_error(y, y_hat))
        r2 = float(r2_score(y, y_hat))

        nonzero = y != 0
        mape = float(np.mean(np.abs((y[nonzero]-y_hat[nonzero]) / y[nonzero])) * 100)

        return RegressionMetrics(
                rmse=rmse,
                mae=mae,
                r2=r2,
                mape=mape,
        )