from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from ml_platform.modeling._core import Predictions

from ml_platform.storage import Storage


@dataclass(frozen=True)
class Residuals:
    df: pd.DataFrame

    def __post_init__(self) -> None:
        required = {"y", "y_hat", "residual"}
        missing = required - set(self.df.columns)

        if missing:
            raise ValueError(f"Residuals missing required columns: {sorted(missing)}")
    
    @property
    def y(self) -> pd.Series:
        return self.df["y"]
    
    @property
    def y_hat(self) -> pd.Series:
        return self.df["y_hat"]
    
    @property
    def residual(self) -> pd.Series:
        return self.df["residual"]
    
    @property
    def row_id(self) -> pd.Series:
        return self.df["row_id"] if "row_id" in self.df.columns else None
    
    @property
    def to_frame(self) -> pd.DataFrame:
        return self.df.copy()


@dataclass(frozen=True)
class ResidualsBuilder:
    def build(
            self,
            *,
            predictions: Predictions,
    ) -> Residuals:
        out = pd.DataFrame(index=predictions.df.index)
        
        out["y"] = predictions.y
        out["y_hat"] = predictions.y_hat
        out["residual"] = out["y"] - out["y_hat"]

        if predictions.row_id is not None:
            out["row_id"] = predictions.row_id

        return Residuals(df=out)


@dataclass(frozen=True)
class ResidualsResolver:
    storage: Storage

    def resolve(
            self,
            *,
            key: str,
    ) -> Residuals:
        return Residuals(self.storage.read_parquet(key=key))