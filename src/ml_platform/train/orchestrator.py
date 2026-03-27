from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from ml_platform.artifacts.predictions import Predictions
from ml_platform.evaluation.evaluator import RegressionEvaluator
from ml_platform.evaluation.schema import RegressionMetrics

from .base import Trainer
from .splitters import Splitter


@dataclass(frozen=True)
class TrainingResult:
    model: object
    predictions: Predictions
    metrics: RegressionMetrics
    feature_cols: list[str]
    train_df: pd.DataFrame
    valid_df: pd.DataFrame


@dataclass(frozen=True)
class TrainingOrchestrator:
    splitter: Splitter
    trainer: Trainer
    evaluator: RegressionEvaluator

    def run(
        self,
        *,
        df: pd.DataFrame,
    ) -> TrainingResult:

        # ---------------------------
        # split
        # ---------------------------

        train_df, valid_df = self.splitter.split(df=df)

        # ---------------------------
        # train + predict
        # ---------------------------

        fit_result = self.trainer.fit(df=train_df)

        predictions = self.trainer.predict(
            model=fit_result.model,
            df=valid_df,
            feature_cols=fit_result.feature_cols,
        )

        # ---------------------------
        # evaluate 
        # ---------------------------

        metrics = self.evaluator.evaluate(predictions=predictions)

        # ---------------------------
        # result 
        # ---------------------------

        return TrainingResult(
            model=fit_result.model,
            predictions=predictions,
            metrics=metrics,
            feature_cols=fit_result.feature_cols,
            train_df=train_df,
            valid_df=valid_df
        )