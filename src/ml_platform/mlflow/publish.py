"""
MLflow tracking utilities.

This module is responsible for publishing training outputs to MLflow as 
immutable evidence.

Responsibilities:
    - Create an MLflow run
    - Log metrics and structured evaluation artifacts
    - Register an immutable model version in the model registry

Out of scope:
    - Alias management or promotion
    - Model comparison or selection logic
    - Serving or deployment concerns
"""
from __future__ import annotations

from typing import Any
import os

import pandas as pd

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient


# --- helpers ---
def _require_env(var: str) -> str:
    v = os.getenv(var, "").strip()
    if not v:
        raise RuntimeError(f"Missing required env var: {var}")
    return v


def _flatten_metrics(metrics: dict) -> dict[str, float]:
    """
    MLflow metrics must be scalar floats. Non-numerics are logged via artifacts.
    """
    out: dict[str, float] = {}
    for k, v in metrics.items():
        if isinstance(v, (int, float)):
            out[k] = float(v)
    return out


def log_and_register_model(
    *,
    model_name: str,
    run_id: str,  # utc
    model: Any,
    metrics: dict,
    preds: pd.DataFrame,
    features: list[str],
    input_key: str,          # pointer to data
    predictions_key: str,    # pointer to preds already written to data store
) -> dict:
    """
    MLflow source-of-truth for Track stage:
      - experiment tracking
      - model registry (version creation)

    This function performs ZERO data-store writes. It only logs pointers.

    NOTE:
        - This does NOT perform model selection.
        - This does NOT promote/alias any model version (SELECT)
    """
    mlflow.set_tracking_uri(_require_env("MLFLOW_TRACKING_URI"))
    mlflow.set_experiment(_require_env("MLFLOW_EXPERIMENT_NAME"))

    registry_root = _require_env("NOWCAST_REGISTRY_MODEL")
    registry_name = f"{registry_root}.{model_name}"

    with mlflow.start_run(run_name=f"{registry_name}:{run_id}") as run:
        mlflow.set_tags(
            {
                "model_family": model_name,
                "registry_model_name": registry_name,
                "run_id": run_id,
                "created_utc": run_id,
                "input_key": input_key,
                "eval.predictions_key": predictions_key,
            }
        )

        mlflow.log_metrics(_flatten_metrics(metrics))

        mlflow.log_dict(
            {
                "model_name": model_name,
                "run_id": run_id,
                "created_utc": run_id,
                "input_key": input_key,
                "predictions_key": predictions_key,
                "metrics": metrics,
            },
            artifact_file="metrics.json",
        )

        mlflow.log_dict(
            {
                "n_rows": int(len(preds)),
                "n_cols": int(preds.shape[1]),
                "columns": list(preds.columns),
            },
            artifact_file="eval_summary.json",
        )

        mlflow.log_dict(
            {
                "features": list(features),
                "n_features": len(features),
            },
            artifact_file="features.json",
        )

        # register model info
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=registry_name,
        )

        client = MlflowClient()
        versions = client.search_model_versions(f"name='{registry_name}'")
        if not versions:
            raise RuntimeError(f"Model registered but no versions found for: {registry_name}")
        
        latest = max(versions, key=lambda mv: int(mv.version))
        version = str(latest.version)

        model_uri = f"models:/{registry_name}/{version}"

        return {
            "mlflow_run_id": run.info.run_id,
            "experiment_id": run.info.experiment_id,
            "registry_model_name": registry_name,
            "registry_model_version": str(version),
            "registry_model_uri": model_uri,
            "predictions_key": predictions_key,
        }