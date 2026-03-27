from __future__ import annotations

from dataclasses import dataclass

from .schema import PredictionsSet, RegressionMetrics
from .scorer import RegressionScorer
from ml_platform.artifacts.predictions import Predictions


@dataclass(frozen=True)
class RegressionEvaluator:
    scorer: RegressionScorer
    prediction_col: str = "y_hat"

    def evaluate(
        self,
        *,
        predictions: Predictions,
    ) -> RegressionMetrics:
        df = predictions.df

        score_df = df[[predictions.target_col, self.prediction_col]].dropna()

        if score_df.empty:
            raise ValueError("No valid rows available for evaluation.")

        prediction_set = PredictionsSet(
            y_true=score_df[predictions.target_col],
            y_hat=score_df[self.prediction_col],
        )

        return self.scorer.score(prediction_set=prediction_set)