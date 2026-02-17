from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd
from sklearn.pipeline import Pipeline

from macro_nowcast.train.models.base import ModelSpec


@dataclass(frozen=True)
class ModelTrainer(ABC):
    """
    Base trainer contract for train components.

    Subclasses implement fit() and predict()
    """

    spec: ModelSpec
    target_col: str
    time_col: str

    @abstractmethod
    def fit(self, df: pd.DataFrame):
        ...
    
    @abstractmethod
    def predict(self, model: Pipeline, df: pd.DataFrame):
        ...
    
    def _split_xy(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        y = df[self.target_col]
        X = df.drop(columns=[self.time_col, self.target_col])
        return X, y