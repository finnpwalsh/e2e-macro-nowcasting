from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .features import FeatureResolver
from ..core.predictions import PredictionsBuilder
from .splitting import Splitter

from .trainer import Trainer
from .contract import TrainingResult


@dataclass(frozen=True)
class TrainingWorkflow:
    feature_resolver: FeatureResolver
    splitter: Splitter
    trainer: Trainer

    def run(
        self,
        *,
        df: pd.DataFrame,
        row_id_col: str | None = None,
    ) -> TrainingResult:
        
        feature_cols = self.feature_resolver.resolve(columns=df.columns)

        train_df, valid_df = self.splitter.split(df=df)

        trained_model = self.trainer.fit(df=train_df, feature_cols=feature_cols)

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

        # -------------------------------
        # result 
        # -------------------------------

        return TrainingResult(
            trained_model=trained_model,
            train_df=train_df,
            valid_df=valid_df,
            predictions=predictions,
        )