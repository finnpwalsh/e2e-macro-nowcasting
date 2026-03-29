from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ml_platform.train import TrainingWorkflow
from ml_platform.artifacts import PredictionsBuilder
from ml_platform.runs import RunTracker

from .schema import TrainEvaluateResult
from .evaluator import RegressionEvaluator


@dataclass(frozen=True)
class TrainEvaluateWorkflow:
    training_workflow: TrainingWorkflow
    predictions_builder: PredictionsBuilder
    evaluator: RegressionEvaluator
    tracker: RunTracker
    
    def run(self, *, df: pd.DataFrame) -> TrainEvaluateResult:
        training_result = self.training_workflow.run(df=df)

        predictions = self.predictions_builder.build(df=df, y_hat=training_result.y_hat)

        metrics = self.evaluator.evaluate(evaluation_input=predictions)

        return TrainEvaluateResult(
            trained_model=training_result.trained_model,
            predictions=predictions,
            metrics=metrics,
        )