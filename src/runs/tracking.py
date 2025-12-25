from __future__ import annotations

from pathlib import Path
from typing import Any

import mlflow

from src.config.paths import ARTIFACTS_DIR

PARAM_KEYS = ("alpha", "split_date", "target")
METRIC_KEYS = ("rmse")

def setup_mlflow_local(experiment: str = "baseline") -> None:
    """
    Set up MLflow to use local / file-based tracking storage under artifacts.
    """
    tracking_dir = ARTIFACTS_DIR / "mlruns"
    mlflow.set_tracking_uri(f"file:{tracking_dir}")
    mlflow.set_experiment(experiment)

def log_run_to_mlflow(
        *,
        run_name: str,
        run_id: str,
        pipeline: str,
        metrics: dict[str, Any],
        artifact_paths: dict[str, Path],
) -> str:
    """
    Create an MLflow run and log params, metrics, and key artifacts.

    Returns the MLflow internal run_id.
    """
    with mlflow.start_run(run_name=run_name) as run:
        # searchable metadata (what it is)
        mlflow.set_tags(
            {
                "app": "e2e-macro-nowcasting",
                "pipeline": pipeline,
                "run_id": run_id,
            }
        )

        # log params (what I chose)
        for key in PARAM_KEYS:
            val = metrics.get(key)
            if val is not None:
                mlflow.log_param(key, val)
        
        # log metrics (coerce int -> float) (how it did)
        for key in METRIC_KEYS:
            val = metrics.get(key)
            if val is None:
                raise KeyError(f"metrics missing required key: {key}")
            mlflow.log_metric(key, float(val))
        
        # log artifacts
        mlflow.log_artifact(str(artifact_paths["model"]), artifact_path="models")
        mlflow.log_artifact(str(artifact_paths["metrics"]), artifact_path="metrics")
        mlflow.log_artifact(str(artifact_paths["preds"]), artifact_path="predictions")

        return run.info.run_id