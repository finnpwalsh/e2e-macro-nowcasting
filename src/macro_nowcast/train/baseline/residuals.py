from __future__ import annotations

from dataclasses import dataclass
import numpy as numpy
import pandas as pd


@dataclass(frozen=True)
class BaselineResiduals:
    """
    Baseline residuals object.

    Contract:
        residual = y - y_hat
    """
    y: pd.Series
    y_hat: pd.Series

    @property
    def residual(self) -> pd.Series:
        return self.y - self.y_hat
    
    def to_frame(self, ds: str = "ds") -> pd.DataFrame:
        return pd.DataFrame(
            {
                ds: self.y.index,
                "y": self.y.values,
                "y_hat": self.y_hat.values,
                "residual": self.residual.values,
            }
        )