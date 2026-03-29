from __future__ import annotations

from typing import Any, Protocol
from dataclasses import dataclass

import pandas as pd


class ModelSpec(Protocol):
    def build(self) -> Any: ...


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