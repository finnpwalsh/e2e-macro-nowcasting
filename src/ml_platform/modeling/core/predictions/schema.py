from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Predictions:
    df: pd.DataFrame

    def __post_init__(self) -> None:
        required = {"y", "y_hat"}
        missing = required - set(self.df.columns)
        if missing:
            raise ValueError(f"Predictions missing required columns: {sorted(missing)}")
        
        if len(self.df) == 0:
            raise ValueError("Predictions cannot be empty.")
    
    @property
    def y(self) -> pd.Series:
        return self.df["y"]
    
    @property
    def y_hat(self) -> pd.Series:
        return self.df["y_hat"]
    
    @property
    def row_id(self) -> pd.Series:
        return self.df["row_id"] if "row_id" in self.df.columns else None
    
    def to_frame(self) -> pd.DataFrame:
        return self.df.copy()