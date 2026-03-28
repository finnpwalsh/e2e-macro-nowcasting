from __future__ import annotations

from typing import Any, Mapping

from .context import RunContext
from .schema import RunManifest, RunSummary, RunPointer, TrackerResult

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
        
        spec: Mapping[str, Any],
        provenance: Mapping[str, Any],
        
        metrics: Mapping[str, Any],
        primary_metric: Mapping[str, Any] | None,
        
        artifact_keys: Mapping[str, Any],
        primary_artifact_key: str | None,
        artifact_writes: list[WriteOp],
        
        
        data_signature: DataSignature,
        feature_signature: FeatureSignature | None = None,
    ) -> TrackerResult:
        manifest = RunManifest(
            run_family=ctx.run_family,
            run_id=ctx.run_id,
            created_at_utc=ctx.created_at_utc,
            
            input_key=input_key,
            
            spec=dict(spec),
            provenance=dict(provenance),
            
            data_signature=data_signature,
            feature_signature=None if feature_signature is None else feature_signature,
            
            artifact_keys=dict(artifact_keys),
            metrics=dict(metrics),
        )

        summary = RunSummary(
            run_family=ctx.run_family,
            run_id=ctx.run_id,
            created_at_utc=ctx.created_at_utc,
            
            input_key=input_key,
            
            primary_metric=None if primary_metric is None else dict(primary_metric),
            primary_artifact_key=primary_artifact_key,
        )

        latest = RunPointer(
            run_family=ctx.run_family,
            run_id=ctx.run_id,
            
            manifest_key=ctx.keys.run.manifest,
            summary_key=ctx.keys.run.summary,
            primary_artifact_key=primary_artifact_key,
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