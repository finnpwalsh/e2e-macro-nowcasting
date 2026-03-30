from __future__ import annotations

from dataclasses import dataclass

from .artifacts import Predictions


@dataclass(frozen=True)
class RegressionMetrics:
    rmse: float
    mae: float
    r2: float
    mape: float | None

    def to_dict(self) -> dict[str, float]:
        out =  {
            "rmse": self.rmse,
            "mae": self.mae,
            "r2": self.r2,
        }
        if self.mape is not None:
            out["mape"] = self.mape
        
        return out


@dataclass(frozen=True)
class RegressionEvaluationResult:
    predictions: Predictions
    metrics: RegressionMetrics