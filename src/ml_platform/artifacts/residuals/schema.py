from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


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