from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from ml_platform.train import Trainer, TrainedModel
from .specs import SklearnModelSpec


@dataclass(frozen=True)
class SklearnTrainer(Trainer):
    spec: SklearnModelSpec
    
    def fit(self, *, df: pd.DataFrame, feature_cols: str) -> TrainedModel:
        feature_cols = self.feature_resolver.resolve(df=df)
        X, y = self._split_xy(df=df, feature_cols=feature_cols)

        model = self.spec.build()
        model.fit(X, y)

        return TrainedModel(
            model=model,
            feature_cols=feature_cols,
        )
    
    def predict(
            self,
            *,
            df: pd.DataFrame,
            trained_model: TrainedModel
    ) -> pd.Series:
        X, _ = self._split_xy(df=df, feature_cols=trained_model.feature_cols)
        y_hat = trained_model.model.predict(X)

        return pd.Series(y_hat, index=df.index)