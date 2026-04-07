from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

from ...core import Metric, Predictions
from .metrics import RegressionMetrics


@dataclass(frozen=True)
class RegressionScorer:
    def score(
            self,
            *,
            predictions: Predictions,
    ) -> RegressionMetrics:
        y = np.asarray(predictions.y)
        y_hat = np.asarray(predictions.y_hat)

        valid = ~np.isnan(y) & ~np.isnan(y_hat)
        if not np.any(valid):
            raise ValueError("Cannot score predictions: all rows contain NaN in y or y_hat.")
        
        y = y[valid]
        y_hat = y_hat[valid]

        rmse = Metric(
            name = "rmse",
            value = float(np.sqrt(mean_squared_error(y, y_hat))),
            higher_is_better=False
        )

        mae = Metric(
            name="mae",
            value=float(mean_absolute_error(y, y_hat)),
            higher_is_better=False,
        )
        
        r2 = Metric(
            name="r2",
            value=float(r2_score(y, y_hat)),
            higher_is_better=True,
        )

        
        nonzero = y != 0

        if not np.any(nonzero):
            mape = None
        else:
            mape = Metric(
                name="mape",
                value=float(np.mean(np.abs((y[nonzero]-y_hat[nonzero]) / y[nonzero])) * 100),
                higher_is_better=False,
    )
    
        return RegressionMetrics(
                rmse=rmse,
                mae=mae,
                r2=r2,
                mape=mape,
        )