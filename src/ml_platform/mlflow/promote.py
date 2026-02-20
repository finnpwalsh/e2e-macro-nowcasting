"""
Mlflow model promotion utilities.

This module provides Select-stage capabilities for mutating deployment
pointers in the MLflow model registry.

Responsibilities:
    - Promote a specified registered model version to a named alias
    - Update registry alias pointers

Out of scope:
    - Model training or evaluation
    - Metric logging or artifact publishing
    - Model comparison beyond "latest wins"
    - Serving or deployment logic

Notes:
    This module mutates control-plane state only (registry aliases).
    All model versions are assumed to have been published and registered
    prior to promotion. 
"""
from __future__ import annotations

import os

import mlflow
from mlflow.tracking import MlflowClient


def _require_env(var: str) -> str:
    v = os.getenv(var, "").strip()
    if not v:
        raise RuntimeError("Missing required env var: {var}")
    return v
    

def promote_latest(
        *,
        model_name: str = "baseline",
) -> dict:
    """Promote the latest registered model version to an alias."""
    registry_root = _require_env("NOWCAST_REGISTRY_MODEL")
    alias = _require_env("NOWCAST_MODEL_ALIAS")

    mlflow.set_tracking_uri(_require_env("MLFLOW_TRACKING_URI"))
    client = MlflowClient()

    registry_name = f"{registry_root}.{model_name}"

    # Resolve latest = max(version)
    versions = client.search_model_versions(f"name='{registry_name}'")
    if not versions:
        raise RuntimeError(f"No model versions found for registry model: {registry_name}")
    
    latest = max(versions, key=lambda mv: int(mv.version))
    latest_version = str(latest.version)

    # Promote (alias mutation)
    client.set_registered_model_alias(
        name=registry_name,
        alias=alias,
        version=latest_version,
    )

    return {
        "registry_model_name": registry_name,
        "alias": alias,
        "version": latest_version,
        "model_uri": f"models:/{registry_name}@{alias}"
    }