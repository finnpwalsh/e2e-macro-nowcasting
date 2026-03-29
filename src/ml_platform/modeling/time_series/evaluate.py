from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ml_platform.modeling._core import TrainingResult
from ml_platform.modeling.regression import PredictionsBuilder, RegressionScorer, RegressionMetrics

from .schema import TimeSeriesEvalResult


@dataclass(frozen=True)
class TimeSeriesEvaluator:
    training_result: TrainingResult
    scorer: RegressionScorer

    def evaluate(self, *, df: pd.DataFrame, target_col: str, time_col: str) -> TimeSeriesEvalResult:
        predictions = PredictionsBuilder(
            target_col=target_col,
            row_id_col=time_col,
        ).build(
            df=df,
            y_hat=self.training_result.y_hat,
        )

        metrics = self.scorer.score(evaluation_input=predictions)

        return TimeSeriesEvalResult(
            traning_result=self.training_result,
            predictions=predictions,
            metrics=metrics,
        )