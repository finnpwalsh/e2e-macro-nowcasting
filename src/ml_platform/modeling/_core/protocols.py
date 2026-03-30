from __future__ import annotations

from typing import Protocol, Mapping, Any

import pandas as pd


class Splitter(Protocol):
    def split(
        self,
        *,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        ...


class FeatureResolver(Protocol): 
    def resolve(self, *, df: pd.DataFrame, target_col: str) -> list[str]: ...


class FitPredictModel(Protocol):
    def fit(
        self,
        *,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> Any:
        ...
    
    def predict(
        self,
        *,
        X: pd.DataFrame,
    ) -> Any:
        ...


class ModelSpec(Protocol):
    def build(
        self,
        *,
        params: Mapping[str, Any] | None = None,
    ) -> FitPredictModel: ...


