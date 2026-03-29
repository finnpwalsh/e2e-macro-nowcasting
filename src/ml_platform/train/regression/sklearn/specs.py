from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sklearn.base import RegressorMixin
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import Ridge


class SklearnModelSpec(Protocol):
    def build(self) -> RegressorMixin: ...


@dataclass(frozen=True)
class RidgeSpec:
    alpha: float = 1.0

    def build(self) -> RegressorMixin:
        return Pipeline(
            steps = [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("ridge", Ridge(alpha=self.alpha)),
            ]
        )