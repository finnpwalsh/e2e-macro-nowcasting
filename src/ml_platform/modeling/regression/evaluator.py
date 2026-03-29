from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

from .schema import RegressionEvaluationInput, RegressionMetrics

from ml_platform.evaluation import Evaluator
from ml_platform.artifacts import Predictions


@dataclass(frozen=True)
class RegressionScorer:
    def score(
            self,
            *,
            evaluation_input: RegressionEvaluationInput,
    ) -> RegressionMetrics:
        y_true = np.asarray(evaluation_input.y_true)
        y_hat = np.asarray(evaluation_input.y_hat)

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


@dataclass(frozen=True)
class RegressionEvaluator(Evaluator(Predictions, RegressionMetrics)):
    scorer: RegressionScorer

    def evaluate(
        self,
        *,
        evaluation_input: Predictions,
    ) -> RegressionMetrics:
        score_df = evaluation_input.df[["y", "y_hat"]].dropna()
        if score_df.empty:
            raise ValueError("No valid rows available for evaluation.")

        regression_input = RegressionEvaluationInput(
            y_true=score_df["y"],
            y_hat=score_df["y_hat"],
        )
        regression_input.validate()

        return self.scorer.score(evaluation_input=regression_input)