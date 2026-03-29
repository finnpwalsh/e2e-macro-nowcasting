from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class RegressionEvaluationInput:
    y_true: pd.Series
    y_hat: pd.Series

    def validate(self) -> None:
        if len(self.y_true) != len(self.y_hat):
            raise ValueError("y_true and y_hat must have the same length.")
        
        if len(self.y_true == 0):
            raise ValueError("Evaluation input empty.")


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