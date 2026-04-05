from __future__ import annotations

from typing import Any, Mapping
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class TrainedModel:
    model: Any
    feature_cols: list[str]
    target_col: str


@dataclass(frozen=True)
class TrainingResult:
    trained_model: TrainedModel
    train_df: pd.DataFrame
    valid_df: pd.DataFrame
    y_hat: pd.Series


@dataclass(frozen=True)
class ModelDefinition:
    engine: str
    name: str
    params: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine": self.name,
            "name": self.name,
            "params": dict(self.params),
        }