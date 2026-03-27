from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from .schema import TrainingResult
from .trainer import Trainer
from .splitters import Splitter

from ml_platform.evaluation import Evaluator


@dataclass(frozen=True)
class TrainingOrchestrator:
    splitter: Splitter
    trainer: Trainer
    evaluator: Evaluator

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
        )