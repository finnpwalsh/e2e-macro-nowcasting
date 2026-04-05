from __future__ import annotations

from dataclasses import dataclass
from abc import ABC

import pandas as pd

from .schema import TrainedModel, TrainingResult
from .protocols import Splitter, FeatureResolver, ModelSpec


@dataclass(frozen=True)
class Trainer(ABC):
    target_col: str
    feature_resolver: FeatureResolver
    model_spec: ModelSpec
    model_params: dict[str, object] | None = None

    def fit(self, *, df: pd.DataFrame) -> TrainedModel:
        feature_cols = self.feature_resolver.resolve(
            df=df,
            target_col=self.target_col,
        )
        X, y = self._split_xy(df=df, feature_cols=feature_cols)

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
    
    def _split_xy(
            self,
            *,
            df: pd.DataFrame,
            feature_cols: list[str],
    ) -> tuple[pd.DataFrame, pd.Series]:
        y = df[self.target_col]
        X = df[feature_cols].copy()
        return X, y


@dataclass(frozen=True)
class TrainingWorkflow:
    splitter: Splitter
    trainer: Trainer

    def run(
        self,
        *,
        df: pd.DataFrame,
    ) -> TrainingResult:

        # -------------------------------
        # split 
        # -------------------------------

        train_df, valid_df = self.splitter.split(df=df)

        # -------------------------------
        # train + predict 
        # -------------------------------

        trained_model = self.trainer.fit(df=train_df)

        y_hat = self.trainer.predict(
            trained_model=trained_model,
            df=valid_df,
        )

        # -------------------------------
        # result 
        # -------------------------------

        return TrainingResult(
            trained_model=trained_model,
            train_df=train_df,
            valid_df=valid_df,
            y_hat=y_hat,
        )