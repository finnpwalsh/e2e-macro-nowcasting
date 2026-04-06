from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .._core import Splitter, Trainer, TrainingResult, PredictionsBuilder


@dataclass(frozen=True)
class TrainingWorkflow:
    splitter: Splitter
    trainer: Trainer

    def run(
        self,
        *,
        df: pd.DataFrame,
        row_id_col: str | None = None,
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
        # build predictions 
        # -------------------------------

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