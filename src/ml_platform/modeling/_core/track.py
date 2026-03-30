from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ml_platform.runs import RunArtifacts, RunContext, RunTracker, TrackerResult
from ml_platform.signatures import DataSignatureBuilder, FeatureSignatureBuilder
from ml_platform.storage.persistence import JoblibWrite, ParquetWrite

from .predictions import Predictions
from .evaluate import Metrics
from .schema import TrainingResult
from .definitions import ModelDefinition


@dataclass(frozen=True)
class TrainingTrackingAdapter:
    tracker: RunTracker
    data_signature_builder: DataSignatureBuilder
    feature_signature_builder: FeatureSignatureBuilder

    def track(
        self,
        *,
        ctx: RunContext,
        df: pd.DataFrame,
        input_key: str,
        model_definition: ModelDefinition,
        predictions: Predictions,
        training_result: TrainingResult,
        metrics: Metrics,
    ) -> TrackerResult:

        artifacts = RunArtifacts(
            primary=ctx.keys.models.model,
            extras={
                "predictions": ctx.keys.datasets.predictions,
            }
        )

        artifact_writes = [
            JoblibWrite(
                key=ctx.keys.models.model,
                payload=training_result.trained_model.model,
            ),
            ParquetWrite(
                key=ctx.keys.datasets.predictions,
                df=predictions.to_frame(),
            ),
        ]

        data_signature = self.data_signature_builder.build(
            df=df,
            train_df=training_result.train_df,
            valid_df=training_result.valid_df,
        )

        feature_signature = self.feature_signature_builder.build(
            df=df,
            feature_cols=training_result.trained_model.feature_cols,
        )

        return self.tracker.track(
            ctx=ctx,
            input_key=input_key,
            spec=model_definition,
            metrics=metrics,
            artifacts=artifacts,
            artifact_writes=artifact_writes,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )