from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ml_platform.modeling._core import TrainingWorkflow

from .schema import TrainEvaluateResult
from .evaluators import RegressionEvaluator
from .builders import PredictionsBuilder


@dataclass(frozen=True)
class RegressionModelingWorkflow:
    training_workflow: TrainingWorkflow
    predictions_builder: PredictionsBuilder
    evaluator: RegressionEvaluator
    
    def run(self, *, df: pd.DataFrame) -> TrainEvaluateResult:
        training_result = self.training_workflow.run(df=df)

        predictions = self.predictions_builder.build(df=df, y_hat=training_result.y_hat)

        metrics = self.evaluator.evaluate(evaluation_input=predictions)

        return TrainEvaluateResult(
            trained_model=training_result.trained_model,
            predictions=predictions,
            metrics=metrics,
        )