from __future__ import annotations

from typing import Any
from dataclasses import dataclass

import pandas as pd

from .predictions import Predictions


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
    predictions: Predictions