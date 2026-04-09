from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ml_platform.modeling.outputs import PredictionsBuilder
from ml_platform.modeling.features import FeatureSelector, FeatureSignatureBuilder

from ml_platform.modeling.training import Trainer
from ml_platform.modeling.splitting import Splitter
from .schema import TrainingResult


@dataclass(frozen=True)
class TrainingService:
    feature_selector: FeatureSelector
    splitter: Splitter
    trainer: Trainer

    def run(
        self,
        *,
        df: pd.DataFrame,
        row_id_col: str | None = None,
    ) -> TrainingResult:
        train_df, valid_df = self.splitter.split(df=df)
        
        feature_cols = self.feature_selector.resolve(columns=train_df.columns)

        trained_model = self.trainer.fit(
            df=train_df,
            feature_cols=feature_cols,
        )

        y_hat = self.trainer.predict(
            trained_model=trained_model,
            df=valid_df,
        )

        predictions = PredictionsBuilder(
            target_col=trained_model.target_col,
            row_id_col=row_id_col,
        ).build(
            df=valid_df,
            y_hat=y_hat,
        )

        feature_signature = FeatureSignatureBuilder().build(
            df=train_df,
            feature_cols=feature_cols,
        )

        return TrainingResult(
            trained_model=trained_model,
            predictions=predictions,
            feature_signature=feature_signature,
        )