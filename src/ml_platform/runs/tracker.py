from __future__ import annotations

from collections.abc import Sequence

from .context import RunContext
from .schema import RunSpec, RunArtifacts, RunManifest, RunSummary, RunPointer, TrackerResult

from ml_platform.modeling._core import Metric, Metrics
from ml_platform.signatures import DataSignature, FeatureSignature
from ml_platform.storage.persistence import (
    PersistencePlan,
    JsonWrite,
    WriteOp,
)


class RunTracker:
    def track(
        self,
        ctx: RunContext,
        *,
        input_key: str,
        
        spec: RunSpec,
        
        metrics: Metrics,
        primary_metric: Metric | None,
        
        run_artifact_keys: RunArtifacts,
        run_artifact_writes: Sequence[WriteOp],
        
        data_signature: DataSignature,
        feature_signature: FeatureSignature | None = None,
    ) -> TrackerResult:
        manifest = RunManifest(
            run_identity=ctx.identity,
            input_key=input_key,
            spec=spec,
            artifacts=run_artifact_keys,
            metrics=metrics,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )

        summary = RunSummary(
            run_identity=ctx.identity,
            input_key=input_key,
            primary_metric=primary_metric,
            primary_artifact_key=run_artifact_keys.primary,
        )

        writes = [
            *run_artifact_writes,
            JsonWrite(key=ctx.keys.run.manifest, payload=manifest),
            JsonWrite(key=ctx.keys.run.summary, payload=summary),
        ]

        return TrackerResult(
            manifest=manifest,
            summary=summary,
            persistence_plan=PersistencePlan(writes=writes),
        )