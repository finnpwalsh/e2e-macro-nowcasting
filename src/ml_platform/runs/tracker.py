from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import pandas as pd

from .context import RunContext
from .manifests import RunManifest, RunSummary, LatestPointer
from .write_plan import WritePlan, JsonWrite, JoblibWrite, ParquetWrite

@dataclass(frozen=True)
class TrackerResult:
    manifest: RunManifest
    summary: RunSummary
    write_plan: WritePlan


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
                "model": ctx.keys.artifacts.model,
                "predictions": ctx.keys.artifacts.predictions,
            },
            metrics=metrics,
        )

        summary = RunSummary(
            model_name=ctx.model_name,
            run_id=ctx.run_id,
            created_at_utc=ctx.created_at_utc,
            input_key=input_key,
            primary_metric={
                "rmse": metrics.get("rmse"),
                "mae": metrics.get("mae"),
            },
            model_artifact_key=ctx.keys.artifacts.model,
        )

        latest = LatestPointer(
            model_name=ctx.model_name,
            run_id=ctx.run_id,
            manifest_key=ctx.keys.run.manifest,
            model_artifact_key=ctx.keys.artifacts.model,
        )

        writes: list[JsonWrite | JoblibWrite | ParquetWrite] [ParquetWrite] = [
            JoblibWrite(key=ctx.keys.artifacts.model, obj=model_obj),
            ParquetWrite(key=ctx.keys.artifacts.predictions, df=predictions_df),
            JsonWrite(key=ctx.keys.run.manifest, payload=manifest),
            JsonWrite(key=ctx.keys.run.summary, payload=summary),
            JsonWrite(key=ctx.keys.pointers.latest, payload=latest),  
        ]

        return TrackerResult(
            manifest=manifest,
            summary=summary,
            write_plan=WritePlan(writes=writes),
        )