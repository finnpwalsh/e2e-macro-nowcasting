from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ..core.models import ModelSpec, TrainedModel


@dataclass(frozen=True)
class Trainer:
    target_col: str
    model_spec: ModelSpec
    model_params: dict[str, object] | None = None

    def fit(self, *, df: pd.DataFrame, feature_cols: list[str]) -> TrainedModel:
        X = df[feature_cols].copy()
        y = df[self.target_col]

        params = self.model_params or {}

        model = self.model_spec.build(params=params)
        model.fit(X, y)

        return TrainedModel(
            model=model,
            feature_cols=feature_cols,
            target_col=self.target_col,
        )

    def predict(
            self,
            *,
            df: pd.DataFrame,
            trained_model: TrainedModel,
    ) -> pd.Series:
        X = df[trained_model.feature_cols].copy()
        y_hat = trained_model.model.predict(X)
        return pd.Series(y_hat, index=df.index, name="y_hat")