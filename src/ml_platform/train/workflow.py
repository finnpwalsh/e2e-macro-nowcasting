from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .schema import TrainingResult
from .trainer import Trainer
from .splitters import Splitter


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
            y_hat=y_hat,
        )