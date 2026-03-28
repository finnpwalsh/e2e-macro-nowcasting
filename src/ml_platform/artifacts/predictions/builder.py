from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import pandas as pd

from .schema import Predictions


@dataclass(frozen=True)
class PredictionsBuilder:
    target_col: str
    row_id_col: str | None = None

    def build(
            self,
            *,
            df: pd.DataFrame,
            y_hat: Any,
    ) -> Predictions:
        if len(df) != len(y_hat): raise ValueError(
            f"Length mismatch: df={len(df)}, y_hat={len(y_hat)}"
        )

        out = pd.DataFrame(index=df.index)
        out["y"] = df[self.target_col].to_numpy()
        out["y_hat"] = pd.Series(y_hat, index=df.index)

        if self.row_id_col is not None:
            out["row_id"] = df[self.row_id_col].to_numpy()

        return Predictions(df=out)