from __future__ import annotations

from typing import Protocol, Any

import pandas as pd


class FitPredictModel(Protocol):
    def fit(
        self,
        *,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> Any:
        ...
    
    def predict(
        self,
        *,
        X: pd.DataFrame,
    ) -> Any:
        ...