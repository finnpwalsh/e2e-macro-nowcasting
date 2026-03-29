from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

from .schema import (
    Predictions,
    RegressionMetrics,
)


@dataclass(frozen=True)
class RegressionScorer:
    def score(
            self,
            *,
            evaluation_input: Predictions,
    ) -> RegressionMetrics:
        y = np.asarray(evaluation_input.y)
        y_hat = np.asarray(evaluation_input.y_hat)

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