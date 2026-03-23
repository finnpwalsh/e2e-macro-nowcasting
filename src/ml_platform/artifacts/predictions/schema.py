from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class Predictions:
    df: pd.DataFrame
    time_col: str
    target_col: str

    def __post_init__(self) -> None:
        required = {self.time_col, self.target_col, "y_hat"}
        missing = required - set(self.df.columns)
        if missing:
            raise ValueError(f"Predictions missing required columns: {sorted(missing)}")

    @property
    def time(self) -> pd.Series:
        return self.df[self.time_col]
    
    @property
    def y(self) -> pd.Series:
        return self.df[self.target_col]
    
    @property
    def y_hat(self) -> pd.Series:
        return self.df["y_hat"]
    
    @property
    def to_frame(self) -> pd.DataFrame:
        return self.df.copy()