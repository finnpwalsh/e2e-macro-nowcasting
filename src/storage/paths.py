"""
Canonical storage paths / keys.

These functions define where things live and do not read or
write data.
"""

from __future__ import annotations

from datetime import datetime, timezone

# ---------------- helpers ----------------

def utc_run_id() -> str:
    """Standard run_id format used across project."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------- Raw Data ---------------

def raw_fred_all() -> str:
    return "data/raw/fred/fred_all.parquet"

def raw_yfinance_all() -> str:
    return "data/raw/yfinance/yf_all.parquet"


# ------------- Processed Data ------------

def processed_fred_wide() -> str:
    return "data/processed/fred_wide.parquet"

def processed_yfinance_features() -> str:
    return "data/processed/yf_features.parquet"

def processed_merged() -> str:
    return "data/processed/merged.parquet"


# ------------ Model Artifacts ------------

def model_dir(model_name: str, run_id: str) -> str:
    return f"artifacts/models/{model_name}/{run_id}"

def model_file(model_name: str, run_id: str) -> str:
    return f"{model_dir(model_name, run_id)}/model.joblib"

def model_metrics(model_name: str, run_id: str) -> str:
    return f"{model_dir(model_name, run_id)}/metrics.json"

def model_latest(model_name: str) -> str:
    return f"artifacts/models/{model_name}/latest.json"


# ------------ Eval Artifacts -------------

def eval_dir(model_name: str, run_id: str) -> str:
    return f"artifacts/eval/{model_name}/{run_id}"

def eval_predictions(model_name: str, run_id: str) -> str:
    return f"{eval_dir(model_name, run_id)}/predictions.parquet"

def eval_summary(model_name: str, run_id: str) -> str:
    return f"{eval_dir(model_name, run_id)}/summary.json"


# ----------- MLflow Artifacts ------------
def mlflow_db() -> str:
    # sqlite backend store file
    return "artifacts/mlflow/mlflow.db"

def mlflow_run_dir(run_id: str) -> str:
    return f"artifacts/mlflow/{run_id}"

def mlflow_model_file(model_name: str, run_id: str) -> str:
    return f"{mlflow_run_dir(run_id)}/models/{model_name}.joblib"

def mlflow_metrics_file(model_name: str, run_id: str) -> str:
    return f"{mlflow_run_dir(run_id)}/metrics/{model_name}.json"

def mlflow_predictions_file(model_name: str, run_id: str) -> str:
    return f"{mlflow_run_dir(run_id)}/predictions/{model_name}.parquet"