from __future__ import annotations

from typing import Any, Protocol
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class TrainedModel:
    model: Any
    feature_cols: list[str]


@dataclass(frozen=True)
class TrainingResult:
    trained_model: TrainedModel
    y_hat: pd.Series


class FeatureResolver(Protocol):
    def resolve(self, *, df: pd.DataFrame) -> list[str]: ...