from __future__ import annotations

from dataclasses import dataclass

from ml_platform.artifacts import Predictions
from ml_platform.evaluation.regression import RegressionMetrics
from ml_platform.train import TrainedModel


@dataclass(frozen=True)
class TrainEvaluateResult:
    trained_model: TrainedModel
    predictions: Predictions
    metrics: RegressionMetrics