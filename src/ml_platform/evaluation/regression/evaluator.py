from __future__ import annotations

from dataclasses import dataclass

from .schema import RegressionEvaluationInput, RegressionMetrics
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

        # ---- required evaluation columns ----
        required_cols = [predictions.target_col, self.prediction_col]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required prediction columns: {missing}")
        
        # ---- enforce not all null ----
        score_df = df[[predictions.target_col, self.prediction_col]].dropna()
        if score_df.empty:
            raise ValueError("No valid rows available for evaluation.")

        # ---- enforce input contract ----
        evaluation_input = RegressionEvaluationInput(
            y_true=score_df[predictions.target_col],
            y_hat=score_df[self.prediction_col],
        )
        evaluation_input.validate()

        # ---- return ----
        return self.scorer.score(evaluation_input=evaluation_input)