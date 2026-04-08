from __future__ import annotations

from dataclasses import dataclass

from ..models import FitPredictModel
from ..outputs import Predictions
from ..metadata import FeatureSignature


@dataclass(frozen=True)
class TrainedModel:
    model: FitPredictModel
    feature_cols: list[str]
    target_col: str


@dataclass(frozen=True)
class TrainingResult:
    trained_model: TrainedModel
    predictions: Predictions
    feature_signature: FeatureSignature