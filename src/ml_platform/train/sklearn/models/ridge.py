from __future__ import annotations

from dataclasses import dataclass

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

from ml_platform.train.training import ModelSpec


@dataclass(frozen=True)
class SKRidgeModelSpec(ModelSpec):
    alpha: float = 1.0

    def build(self) -> Pipeline:
        return Pipeline(
            steps = [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("ridge", Ridge(alpha=self.alpha)),
            ]
        )