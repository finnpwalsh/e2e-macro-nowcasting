from __future__ import annotations

import pandas as pd

from ml_platform.runs import RunContext, RunTracker, TrackerResult
from .._core import ModelDefinition, TrainingResult, Metrics

from .builder import TrainingRunArtifactsBuilder


class TrainingRunTracker:
    builder: TrainingRunArtifactsBuilder = TrainingRunArtifactsBuilder()
    tracker: RunTracker = RunTracker()

    def track(
            self,
            *,
            ctx: RunContext,
            df: pd.DataFrame,
            input_key: str,
            model_definition: ModelDefinition,
            training_result: TrainingResult,
            metrics: Metrics,
    ) -> TrackerResult:
        training_artifacts = self.builder.build(
            ctx=ctx,
            df=df,
            training_result=training_result,
        )

        return self.tracker.track(
            ctx=ctx,
            input_key=input_key,
            spec=model_definition,
            metrics=metrics,
            artifacts=training_artifacts.artifacts,
            artifact_writes=training_artifacts.writes,
            data_signature=training_artifacts.data_signature,
            feature_signature=training_artifacts.feature_signature,
        )