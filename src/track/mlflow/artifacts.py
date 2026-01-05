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
    promote: bool | None = None,
) -> dict:
    """
    MLflow source-of-truth:
      - experiment tracking
      - model registry
      - alias promotion / rollback primitive

    This function performs ZERO data-store writes. It only logs pointers.
    """
    tracking_uri = _require_env("MLFLOW_TRACKING_URI")
    mlflow.set_tracking_uri(tracking_uri)

    exp_name = _require_env("MLFLOW_EXPERIMENT_NAME")
    mlflow.set_experiment(exp_name)

    registry_name = os.getenv("MLFLOW_REGISTRY_MODEL_NAME", model_name)
    alias_name = os.getenv("MLFLOW_MODEL_ALIAS", "champion")
    promote = True if promote is None else bool(promote)

    # canonical model uri for serving (alias-based)
    model_uri = f"models:/{registry_name}@{alias_name}"

    with mlflow.start_run(run_name=f"{model_name}:{run_id}") as run:
        mlflow.set_tags(
            {
                "model_name": model_name,
                "run_id": run_id,
                "input_key": input_key,
                "eval.predictions_key": predictions_key,
                "deploy.model_uri": model_uri,
                "deploy.promote": str(promote).lower(),
            }
        )

        # metrics (scalar only)
        mlflow.log_metrics(_flatten_metrics(metrics))

        # metrics (structured artifact)
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

        # minimal eval summary (derived from preds, but not writing preds)
        mlflow.log_dict(
            {
                "n_rows": int(len(preds)),
                "n_cols": int(preds.shape[1]),
                "columns": list(preds.columns),
            },
            artifact_file="eval_summary.json",
        )

        # feature schema
        mlflow.log_dict(
            {
                "features": list(features),
                "n_features": len(features),
            },
            artifact_file="features.json",
        )

        # model -> MLflow + registry
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=registry_name,
        )

        client = MlflowClient()

        version = getattr(model_info, "registered_model_version", None)
        if version is None:
            hits = client.search_model_versions(
                f"name='{registry_name}' and run_id='{run.info.run_id}'"
            )
            if not hits:
                raise RuntimeError(
                    "Model registered but could not resolve version for alias assignment."
                )
            version = hits[0].version

        if promote:
            client.set_registered_model_alias(
                name=registry_name,
                alias=alias_name,
                version=str(version),
            )

        return {
            "mlflow_run_id": run.info.run_id,
            "experiment_id": run.info.experiment_id,
            "registry_model_name": registry_name,
            "registry_model_version": str(version),
            "alias": alias_name,
            "model_uri": model_uri,
            "promoted": promote,
            "predictions_key": predictions_key,
        }