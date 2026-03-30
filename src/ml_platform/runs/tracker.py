from __future__ import annotations

from collections.abc import Sequence

from .context import RunContext
from .schema import RunSpec, RunArtifacts, RunManifest, RunSummary, TrackerResult

from ml_platform.modeling._core import Metrics
from ml_platform.signatures import DataSignature, FeatureSignature
from ml_platform.storage import (
    PersistencePlan,
    JsonWrite,
    WriteOp,
)


class RunTracker:
    def track(
        self,
        *,
        ctx: RunContext,
        input_key: str,
        
        spec: RunSpec,
        
        metrics: Metrics,
        primary_metric_name: str | None,
        
        artifacts: RunArtifacts,
        artifact_writes: Sequence[WriteOp],
        
        data_signature: DataSignature,
        feature_signature: FeatureSignature | None = None,
    ) -> TrackerResult:
        primary_metric = (
            metrics.get_value(name=primary_metric_name)
            if primary_metric_name is not None
            else None
        )
        
        manifest = RunManifest(
            run_identity=ctx.identity,
            input_key=input_key,
            spec=spec,
            artifacts=artifacts,
            metrics=metrics,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )

        summary = RunSummary(
            run_identity=ctx.identity,
            input_key=input_key,
            primary_metric=primary_metric,
            primary_artifact_key=artifacts.primary,
        )

        writes = [
            *artifact_writes,
            JsonWrite(key=ctx.keys.run.manifest, payload=manifest),
            JsonWrite(key=ctx.keys.run.summary, payload=summary),
        ]

        return TrackerResult(
            manifest=manifest,
            summary=summary,
            persistence_plan=PersistencePlan(writes=writes),
        )