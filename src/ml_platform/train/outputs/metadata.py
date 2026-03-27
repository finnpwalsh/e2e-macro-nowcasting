from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from ml_platform.artifacts.predictions import Predictions


@dataclass(frozen=True)
class DataSignature:
    n_rows: int
    n_train: int
    n_valid: int
    columns: list[str]
    dtypes: dict[str, str]
    time_min: str
    time_max: str
    row_fingerprint: str


@dataclass(frozen=True)
class FeatureSignature:
    n_features: int
    features: list[str]
    feature_dtypes: dict[str, str]
    null_counts: dict[str, int]
    feature_fingerprint: str


@dataclass(frozen=True)
class TrainingProvenance:
    generator: str
    trainer: str
    model_name: str
    time_col: str
    target_col: str
    split_date: str


@dataclass(frozen=True)
class TrainingOutputs:
    spec: dict[str, Any]
    provenance: TrainingProvenance
    model: Any
    metrics: dict[str, float]
    predictions: Predictions
    data_signature: DataSignature
    feature_signature: FeatureSignature