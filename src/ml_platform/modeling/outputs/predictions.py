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


@dataclass(frozen=True)
class PredictionsBuilder:
    target: str
    row_id: str | None = None

    def build(
            self,
            *,
            df: pd.DataFrame,
            y_hat: pd.Series,
    ) -> Predictions:
        if len(df) != len(y_hat): raise ValueError(
            f"Length mismatch: df={len(df)}, y_hat={len(y_hat)}"
        )

        out = pd.DataFrame(index=df.index)
        out["y"] = df[self.target].to_numpy()
        out["y_hat"] = pd.Series(y_hat, index=df.index)

        if self.row_id is not None:
            out["row_id"] = df[self.row_id].to_numpy()

        return Predictions(df=out)