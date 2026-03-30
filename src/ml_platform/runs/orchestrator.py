from __future__ import annotations

from dataclasses import dataclass

from ml_platform.runs import RunTracker, TrackerResult
from ml_platform.signatures import DataSignatureBuilder, FeatureSignatureBuilder

from .schema import TrackingInput


@dataclass(frozen=True)
class TrackingOrchestrator:
    tracker: RunTracker
    data_signature_builder: DataSignatureBuilder
    feature_signature_builder: FeatureSignatureBuilder | None = None

    def run(self, tracking_input: TrackingInput) -> TrackerResult:
        data_signature = self.data_signature_builder.build(
            df=tracking_input.full_df,
            train_df=tracking_input.train_df,
            valid_df=tracking_input.valid_df,
        )

        feature_signature = None
        if (
            self.feature_signature_builder is not None
            and tracking_input.feature_cols is not None
        ):
            feature_signature = self.feature_signature_builder.build(
                feature_cols=list(tracking_input.feature_cols)
            )

        return self.tracker.track(
            ctx=tracking_input.ctx,
            input_key=tracking_input.input_key,
            spec=tracking_input.spec,
            run_config=tracking_input.run_config,
            metrics=tracking_input.metrics,
            artifacts=tracking_input.artifacts,
            artifact_writes=tracking_input.artifact_writes,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )