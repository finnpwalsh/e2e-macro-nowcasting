from __future__ import annotations

from dataclasses import dataclass

from ml_platform.modeling.training import TrainedModel
from ml_platform.modeling.outputs import Predictions
from ml_platform.modeling.contracts import FeatureSignature


@dataclass(frozen=True)
class TrainingResult:
    trained_model: TrainedModel
    predictions: Predictions
    feature_signature: FeatureSignature