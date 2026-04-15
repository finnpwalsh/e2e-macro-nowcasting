from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from .predictions import Predictions


@dataclass(frozen=True)
class Residuals:
    df: pd.DataFrame

    def __post_init__(self) -> None:
        required = {"y", "y_hat", "residual"}
        missing = required - set(self.df.columns)

        if missing:
            raise ValueError(f"Residuals missing required columns: {sorted(missing)}")
        
        df = self.df.copy()

        for col in ["y", "y_hat", "residual"]:
            df[col] = pd.to_numeric(df[col], errors="raise")

        if len(df) == 0:
            raise ValueError("Residuals cannot be empty.")
        
        object.__setattr__(self, "df", df)
    

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
    def row_id(self) -> pd.Series | None:
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