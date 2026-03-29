from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any

from sklearn.base import RegressorMixin
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import Ridge


@dataclass(frozen=True)
class RidgeSpec:

    def build(self, *, params: Mapping[str, Any] | None = None) -> RegressorMixin:
        params = params or {}

        alpha=float(params.get("alpha", 1.0))

        return Pipeline(
            steps = [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("ridge", Ridge(alpha=alpha)),
            ]
        )