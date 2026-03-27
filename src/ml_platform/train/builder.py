from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import pandas as pd

from ml_platform.artifacts.predictions import PredictionsBuilder

from ml_platform.train.metadata import TrainingOutputs
from ml_platform.train.builders import (
    DataSignatureBuilder,
    FeatureSignatureBuilder,
    TrainingProvenanceBuilder,
)
from .training import Trainer
from .splitters import Splitter
from ml_platform.evaluation.scorer import RegressionScorer
from ml_platform.evaluation.schema import PredictionSet, RegressionMetrics


@dataclass(frozen=True)
class TrainingBuilder:
    model_name: str
    time_col: str
    target_col: str
    split_date: str

    splitter: Splitter
    trainer: Trainer
    scorer: RegressionScorer

    def run(
        self,
        *,
        df: pd.DataFrame,
    ) -> TrainingOutputs:

        # ---------------------------
        # Split
        # ---------------------------

        train_mask, valid_mask = self.splitter.split_mask(
            df=df,
            split_date=self.split_date,
        )

        train_df = df.loc[train_mask].copy()
        valid_df = df.loc[valid_mask].copy()

        if train_df.empty or valid_df.empty:
            raise ValueError(f"Empty split: train={len(train_df)}, valid={len(valid_df)}")

        # ---------------------------
        # Train + predict
        # ---------------------------

        fit_result = self.trainer.fit(df=train_df)
        model = fit_result.model
        feature_cols = fit_result.feature_cols

        y_hat = self.trainer.predict(
            model=model,
            df=valid_df,
            feature_cols=feature_cols,
        )

        # ---------------------------
        # Predictions artifact
        # ---------------------------

        predictions = PredictionsBuilder(
            time_col=self.time_col,
            target_col=self.target_col,
        ).build(
            df=valid_df,
            y_hat=y_hat,
        )

        pred_df = predictions.df

        # ---------------------------
        # Metrics
        # ---------------------------

        prediction_set = PredictionSet(
            y_true=pred_df[[self.target_col]].dropna(),
            y_hat=pred_df[["y_hat"]].dropna(),
        )

        metrics = self.scorer.score(prediction_set=prediction_set)

        # ---------------------------
        # Metadata
        # ---------------------------

        provenance = TrainingProvenanceBuilder(
            generator_name=self.__class__.__name__,
            trainer_name=self.trainer.__class__.__name__,
            model_name=self.model_name,
            time_col=self.time_col,
            target_col=self.target_col,
            split_date=self.split_date,
        ).build()

        data_signature = DataSignatureBuilder(
            time_col=self.time_col,
            target_col=self.target_col,
        ).build(
            df=df,
            train_df=train_df,
            valid_df=valid_df,
        )

        feature_signature = FeatureSignatureBuilder().build(
            df=df,
            feature_cols=feature_cols,
        )

        return TrainingOutputs(
            spec=asdict(self.trainer.spec),
            provenance=provenance,
            model=model,
            metrics=asdict(metrics),
            predictions=predictions,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )