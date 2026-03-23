from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class Predictions:
    df: pd.DataFrame
    time_col: str
    target_col: str

    @property
    def y(self) -> pd.Series:
        return self.df[self.target_col]
    
    @property
    def y_hat(self) -> pd.Series:
        return self.df["y_hat"]