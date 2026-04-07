from __future__ import annotations

from dataclasses import dataclass

from ..core import Metric


@dataclass(frozen=True)
class RegressionMetrics:
    rmse: Metric
    mae: Metric
    r2: Metric
    mape: Metric | None

    def to_dict(self) -> dict[str, float]:
        out =  {
            "rmse": self.rmse.value,
            "mae": self.mae.value,
            "r2": self.r2.value,
        }
        if self.mape is not None:
            out["mape"] = self.mape.value
        
        return out
    
    def get_metric(self, *, metric: str) -> Metric | None:
        metric = metric.strip().lower()
        match metric:
            case "rmse":
                return self.rmse
            case "mae":
                return self.mae
            case "r2":
                return self.r2
            case "mape":
                return self.mape
            case _:
                raise KeyError(f"Unknown metric: {metric}")