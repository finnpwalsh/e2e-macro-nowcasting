from __future__ import annotations

from dataclasses import dataclass

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

from .base import ModelSpec


@dataclass(frozen=True)
class RidgeModelSpec(ModelSpec):
    alpha: float = 1.0

    def make_pipeline(self) -> Pipeline:
        return Pipeline(
            steps = [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("ridge", Ridge(alpha=self.alpha)),
            ]
        )