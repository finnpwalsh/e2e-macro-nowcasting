from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class Residuals:
    df: pd.DataFrame
    time_col: str

    def __post_init__(self) -> None:
        required = {self.time_col, "y", "y_hat", "residual"}
        missing = required - set(self.df.columns)

        if missing:
            raise ValueError(f"Residuals missing required columns: {sorted(missing)}")
    
    @property
    def time(self) -> pd.Series:
        return self.df[self.time_col]
    
    @property
    def y_hat(self) -> pd.Series:
        return self.df["y_hat"]
    
    @property
    def residual(self) -> pd.Series:
        return self.df["residual"]
    
    @property
    def to_frame(self) -> pd.DataFrame:
        return self.df.copy()