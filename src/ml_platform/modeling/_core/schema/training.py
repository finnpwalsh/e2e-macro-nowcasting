from __future__ import annotations

from typing import Any, Protocol, Mapping
from dataclasses import dataclass

import pandas as pd


class FitPredictModel(Protocol):
    def fit(self, X, y): ...
    def predict(self, X, y): ...


class ModelSpec(Protocol):
    def build(
        self,
        *,params: Mapping[str, Any] | None = None,
    ) -> FitPredictModel: ...


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