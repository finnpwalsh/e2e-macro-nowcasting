from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd

from .schema import TrainedModel
from .components import ModelSpec, FeatureResolver


@dataclass(frozen=True)
class Trainer(ABC):
    spec: ModelSpec
    target_col: str
    feature_resolver: FeatureResolver

    @abstractmethod
    def fit(self, *, df: pd.DataFrame) -> TrainedModel:
        raise NotImplementedError
    
    @abstractmethod
    def predict(
            self,
            *,
            df: pd.DataFrame,
            trained_model: TrainedModel,
    ) -> pd.Series:
        raise NotImplementedError
    
    def _split_xy(
            self,
            *,
            df: pd.DataFrame,
            feature_cols: list[str],
    ) -> tuple[pd.DataFrame, pd.Series]:
        y = df[self.target_col]
        X = df[feature_cols].copy()
        return X, y