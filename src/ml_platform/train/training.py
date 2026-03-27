from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol

import pandas as pd


class ModelSpec(Protocol):
    def build(self) -> Any: ...


class FeatureResolver(Protocol):
    def resolve(self, *, pd.DataFrame) -> list[str]: ...


@dataclass(frozen=True)
class FitResult:
    model: Any
    feature_cols: list[str]


@dataclass(frozen=True)
class Trainer(ABC):
    spec: ModelSpec
    target_col: str
    feature_resolver: FeatureResolver

    @abstractmethod
    def fit(self, *, df: pd.DataFrame) -> FitResult:
        raise NotImplementedError
    
    @abstractmethod
    def predict(
            self,
            *,
            model: Any,
            df: pd.DataFrame,
            feature_cols: list[str]
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