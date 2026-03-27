from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from ml_platform.evaluation.evaluator import RegressionEvaluator

from .outputs.assembler import TrainingOutputsAssembler
from .outputs.metadata import TrainingOutputs
from .engines.base import Trainer
from .splitters import Splitter


@dataclass(frozen=True)
class TrainingOrchestrator:
    model_name: str

    splitter: Splitter
    trainer: Trainer

    evaluator: RegressionEvaluator
    outputs_assembler: TrainingOutputsAssembler

    def run(
        self,
        *,
        df: pd.DataFrame,
    ) -> TrainingOutputs:

        # ---------------------------
        # split
        # ---------------------------

        train_df, valid_df = self.splitter.split(df=df)

        # ---------------------------
        # Train + predict
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
        # assemble 
        # ---------------------------

        return self.outputs_assembler.assemble(
            df=df,
            train_df=train_df,
            valid_df=valid_df,
            trainer=self.trainer,
            model=fit_result.model,
            predictions=predictions,
            metrics=metrics,
            feature_cols=fit_result.feature_cols,
        )