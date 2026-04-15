from __future__ import annotations

from dataclasses import dataclass

from ..models import FitPredictModel


@dataclass(frozen=True)
class FittedModel:
    model: FitPredictModel
    feature_cols: tuple[str, ...]
    target_col: str