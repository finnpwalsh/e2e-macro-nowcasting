from __future__ import annotations

from dataclasses import dataclass

from .protocols import FitPredictModel


@dataclass(frozen=True)
class TrainedModel:
    model: FitPredictModel
    feature_cols: list[str]
    target_col: str