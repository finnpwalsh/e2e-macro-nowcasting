from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Mapping, Any

import pandas as pd


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


@dataclass(frozen=True)
class ModelDefinition:
    engine: str
    name: str
    params: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine": self.engine,
            "name": self.name,
            "params": dict(self.params),
        }