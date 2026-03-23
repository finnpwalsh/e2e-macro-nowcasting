from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.pipeline import Pipeline

from macro_nowcast.train.models.base import ModelSpec


@dataclass(frozen=True)
class Trainer:

    spec: ModelSpec
    target_col: str
    time_col: str

    def fit(self, df: pd.DataFrame) -> Pipeline:
        X, y = self._split_xy(df)

        model = self.spec.make_pipeline()
        model.fit(X, y)

        return model
    

    def predict(self, *, model: Pipeline, df: pd.DataFrame) -> pd.Series:
        X, _ = self._split_xy(df)
        y_hat = model.predict(X)
        
        return pd.Series(y_hat, index=df.index)
    

    def _split_xy(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        y = df[self.target_col]
        X = df.drop(columns=[self.time_col, self.target_col])
        return X, y