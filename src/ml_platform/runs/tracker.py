from __future__ import annotations

from collections.abc import Sequence

from .context import RunContext
from .schema import RunSpec, ArtifactKeys, RunManifest, RunSummary, RunPointer, TrackerResult

from ml_platform.evaluation import Metric, Metrics
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
        
        artifact_keys: ArtifactKeys,
        artifact_writes: Sequence[WriteOp],
        
        
        data_signature: DataSignature,
        feature_signature: FeatureSignature | None = None,
    ) -> TrackerResult:
        manifest = RunManifest(
            run_identity=ctx.identity,
            input_key=input_key,
            spec=spec,
            artifact_keys=artifact_keys,
            metrics=metrics,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )

        summary = RunSummary(
            run_identity=ctx.identity,
            input_key=input_key,
            primary_metric=primary_metric,
            primary_artifact_key=artifact_keys.primary,
        )

        latest = RunPointer(
            run_identity=ctx.identity,
            manifest_key=ctx.keys.run.manifest,
            summary_key=ctx.keys.run.summary,
            primary_artifact_key=artifact_keys.primary,
        )

        writes = [
            *artifact_writes,
            JsonWrite(key=ctx.keys.run.manifest, payload=manifest),
            JsonWrite(key=ctx.keys.run.summary, payload=summary),
            JsonWrite(key=ctx.keys.pointers.latest, payload=latest),  
        ]

        return TrackerResult(
            manifest=manifest,
            summary=summary,
            persistence_plan=PersistencePlan(writes=writes),
        )