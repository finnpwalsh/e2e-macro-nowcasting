from __future__ import annotations

from typing import Protocol
from dataclasses import dataclass

import numpy as np

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

from .schema import PredictionSet, RegressionMetrics


class RegressionScorer(Protocol):
    def score(
            self,
            *,
            prediction_set: PredictionSet,
    ) -> RegressionMetrics: ...


@dataclass(frozen=True)
class DefaultRegressionScorer:
    def score(
            self,
            *,
            prediction_set: PredictionSet,
    ) -> RegressionMetrics:
        y_true = np.asarray(prediction_set.y_true)
        y_hat = np.asarray(prediction_set.y_hat)

        rmse = float(np.sqrt(mean_squared_error(y_true, y_hat)))
        mae = float(mean_absolute_error(y_true, y_hat))
        r2 = float(r2_score(y_true, y_hat))

        nonzero = y_true != 0
        mape = float(np.mean(np.abs((y_true[nonzero]-y_hat[nonzero]) / y_true[nonzero])) * 100)

        return RegressionMetrics(
                rmse=rmse,
                mae=mae,
                r2=r2,
                mape=mape,
        )