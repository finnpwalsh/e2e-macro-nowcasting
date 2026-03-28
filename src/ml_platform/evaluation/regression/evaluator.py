from __future__ import annotations

from dataclasses import dataclass

from .schema import RegressionEvaluationInput, RegressionMetrics
from .scorer import RegressionScorer

from ml_platform.evaluation import Evaluator
from ml_platform.artifacts import Predictions


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