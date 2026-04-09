from __future__ import annotations

from dataclasses import dataclass

from ml_platform.platform.contracts import DataSignature
from ml_platform.platform.runs import RunManifest, RunSummary

from ml_platform.modeling.models import ModelDefinition
from ml_platform.modeling.features import FeatureSignature
from ml_platform.modeling.scoring import Metrics


@dataclass(frozen=True)
class TrainingRunRefs:
    input_key: str


@dataclass(frozen=True)
class TrainingRunConfig:
    target_col: str
    feature_cols: tuple[str, ...] | None = None


@dataclass(frozen=True)
class TrainingRunSpec:
    model_definition: ModelDefinition
    training_config: TrainingRunConfig


@dataclass(frozen=True)
class TrainingRunOutputs:
    model: str
    predictions: str


@dataclass(frozen=True)
class TrainingSummary:
    metrics: Metrics
    primary_artifact_key: str | None


TrainingRunSummary = RunSummary[TrainingRunRefs, TrainingSummary]


@dataclass(frozen=True)
class TrainingRunManifest(
    RunManifest[TrainingRunRefs, TrainingRunSpec, TrainingRunOutputs]
):
    data_signature: DataSignature
    feature_signature: FeatureSignature | None = None