from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ml_platform.runs import RunArtifacts, RunContext, RunTracker, TrackerResult
from ml_platform.signatures import DataSignatureBuilder, FeatureSignatureBuilder
from ml_platform.storage.persistence import JoblibWrite, ParquetWrite

from .schema import TimeSeriesTrainingConfig, TimeSeriesEvalResult


@dataclass(frozen=True)
class TimeSeriesTrackingAdapter:
    tracker: RunTracker
    data_signature_builder: DataSignatureBuilder
    feature_signature_builder: FeatureSignatureBuilder

    def track(
        self,
        *,
        ctx: RunContext,
        df: pd.DataFrame,
        input_key: str,
        config: TimeSeriesTrainingConfig,
        result: TimeSeriesEvalResult,
        primary_metric_name: str | None,
    ) -> TrackerResult:
        model_key = ctx.keys.models.model
        predictions_key = ctx.keys.datasets.predictions

        artifacts = RunArtifacts(
            primary=model_key,
            extras={
                "model": model_key,
                "predictions": predictions_key,
            }
        )
        artifact_writes = [
            JoblibWrite(
                key=model_key,
                payload=result.training_result.trained_model.model,
            ),
            ParquetWrite(
                key=predictions_key,
                df=result.predictions.to_frame(),
            ),
        ]

        data_signature = self.data_signature_builder.build(
            df=df,
            train_df=result.training_result.train_df,
            valid_df=result.training_result.valid_df,
        )

        feature_signature = self.feature_signature_builder.build(
            df=df,
            feature_cols=result.training_result.trained_model.feature_cols,
        )

        return self.tracker.track(
            ctx=ctx,
            input_key=input_key,
            metrics=result.metrics,
            spec=config.spec,
            metrics=result.metrics,
            primary_metric_name=primary_metric_name,
            artifacts=artifacts,
            artifact_writes=artifact_writes,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )