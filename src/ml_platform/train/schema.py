from __future__ import annotations

from typing import Any
from dataclasses import dataclass

from ml_platform.evaluation.base import Metrics
from ml_platform.artifacts.predictions import Predictions


@dataclass(frozen=True)
class TrainedModel:
    model: Any
    feature_cols: list[str]


@dataclass(frozen=True)
class TrainingResult:
    model: object
    predictions: Predictions
    metrics: Metrics
    feature_cols: list[str]