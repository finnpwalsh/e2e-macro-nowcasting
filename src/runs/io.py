from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.pipelines.paths import get_run_dir, get_artifact_dirs

def write_run_meta(
        run_id: str,
        metrics: dict[str, Any],
        pipeline: str,
) -> Path:
    """
    Write run-level metadata to artifacts/{run_id}/run.json
    """
    run_dir = get_run_dir(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)

    run_meta = {
        "run_id": run_id,
        "pipeline": pipeline,
        "target": metrics.get("target"),
        "split_date": metrics.get("split_date"),
        "alpha": metrics.get("alpha"),
    }

    outpath = run_dir / "run.json"
    outpath.write_text(json.dumps(run_meta, indent = 2) + "\n")


def write_run_artifacts(
        *,
        run_id: str,
        model: Any,
        metrics: dict[str, Any],
        preds: pd.DataFrame,
        artifact_name: str,
) -> dict[str, Any]:
    # get directories
    model_dir, metrics_dir, preds_dir = get_artifact_dirs(run_id)

    # make directories
    model_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    preds_dir.mkdir(parents=True, exist_ok=True)

    # make paths
    model_path = model_dir / f"{artifact_name}.joblib"
    metrics_path = metrics_dir / f"{artifact_name}.json"
    preds_path = preds_dir / f"{artifact_name}.parquet"

    # out
    joblib.dump(model, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n")
    preds.to_parquet(preds_path, index=False)

    return{
        "model": model_path,
        "metrics": metrics_path,
        "predictions": preds_path,
    }

