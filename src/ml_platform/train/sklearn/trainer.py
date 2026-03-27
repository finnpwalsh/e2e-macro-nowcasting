from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import pandas as pd

from ml_platform.train.training import FitResult, Trainer


@dataclass(frozen=True)
class SklearnTrainer(Trainer):

    def fit(self, *, df: pd.DataFrame) -> FitResult:
        feature_cols = self.feature_resolver.resolve(df=df)
        X, y = self._split_xy(df=df, feature_cols=feature_cols)

        model = self.spec.build()
        model.fit(X, y)

        return FitResult(
            model=model,
            feature_cols=feature_cols,
        )
    
    def predict(
            self,
            *,
            model: Any,
            df: pd.DataFrame,
            feature_cols: list[str]
    ) -> pd.Series:
        X, _ = self._split_xy(df=df, feature_cols=feature_cols)
        y_hat = model.predict(X)

        return pd.Series(y_hat, index=df.index)