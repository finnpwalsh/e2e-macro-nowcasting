from __future__ import annotations

from dataclasses import dataclass

from .artifacts import Predictions
from .evaluation import RegressionMetrics

from ml_platform.modeling._core import TrainedModel


@dataclass(frozen=True)
class TrainEvaluateResult:
    trained_model: TrainedModel
    predictions: Predictions
    metrics: RegressionMetrics