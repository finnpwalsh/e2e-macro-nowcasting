from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class RegressionMetrics:
    rmse: float
    mae: float
    r2: float
    mape: float | None


@dataclass(frozen=True)
class PredictionsSet:
    y_true: pd.Series
    y_hat: pd.Series