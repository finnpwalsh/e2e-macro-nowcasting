from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import pandas as pd

from .context import RunContext
from .manifests import RunManifest, RunSummary, Pointer
from ml_platform.storage.persistence import PersistencePlan, JsonWrite, JoblibWrite, ParquetWrite


@dataclass(frozen=True)
class TrackerResult:
    manifest: RunManifest
    summary: RunSummary
    persistence_plan: PersistencePlan


class RunTracker:
    def track(
        self,
        ctx: RunContext,
        *,
        input_key: str,
        split_date: str,
        spec: Mapping[str, Any],
        provenance: Mapping[str, Any],
        metrics: Mapping[str, Any],
        model_obj: Any,
        predictions_df: pd.DataFrame,
        data_signature: Mapping[str, Any],
        feature_signature: Mapping[str, Any],
    ) -> TrackerResult:
        manifest = RunManifest(
            model_name=ctx.model_name,
            run_id=ctx.run_id,
            created_at_utc=ctx.created_at_utc,
            
            input_key=input_key,
            split_date=split_date,
            
            spec=spec,
            provenance=provenance,
            
            data_signature=data_signature,
            feature_signature=feature_signature,
            
            artifacts={
                "model": ctx.keys.models.model,
                "predictions": ctx.keys.datasets.predictions,
            },
            metrics=metrics,
        )

        summary = RunSummary(
            model_name=ctx.model_name,
            run_id=ctx.run_id,
            created_at_utc=ctx.created_at_utc,
            
            input_key=input_key,
            split_date=split_date,
            
            primary_metric={
                "rmse": metrics.get("rmse"),
                "mae": metrics.get("mae"),
            },
            model_artifact_key=ctx.keys.models.model,
        )

        latest = Pointer(
            model_name=ctx.model_name,
            run_id=ctx.run_id,
            
            manifest_key=ctx.keys.run.manifest,
            summary_key=ctx.keys.run.summary,
            model_artifact_key=ctx.keys.models.model,
        )

        writes = [
            JoblibWrite(key=ctx.keys.models.model, obj=model_obj),
            ParquetWrite(key=ctx.keys.datasets.predictions, df=predictions_df),
            JsonWrite(key=ctx.keys.run.manifest, payload=manifest),
            JsonWrite(key=ctx.keys.run.summary, payload=summary),
            JsonWrite(key=ctx.keys.pointers.latest, payload=latest),  
        ]

        return TrackerResult(
            manifest=manifest,
            summary=summary,
            persistence_plan=PersistencePlan(writes=writes),
        )