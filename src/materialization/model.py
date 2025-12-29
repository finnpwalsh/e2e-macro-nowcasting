from __future__ import annotations

from typing import Any
import pandas as pd

from src.storage.base import Storage
from src.storage.io import write_joblib, write_json
from src.storage.paths import (
    model_file, 
    model_latest, 
    model_metrics, 
    eval_predictions,
)

def write_model_artifacts(
        *,
        storage: Storage,
        model_name: str,
        run_id: str, # utc
        model: Any,
        metrics: dict,
        preds: pd.DataFrame,
) -> dict:
    """
    Write canonical artifacts for the inputted model.

    Returns a dict of written storage keys for easy printing/testing.
    """
    # define canonical keys
    k_model = model_file(model_name, run_id)
    k_metrics = model_metrics(model_name, run_id)
    k_latest = model_latest(model_name)
    k_preds = eval_predictions(model_name, run_id)

    # model
    write_joblib(storage, k_model, model)

    # metrics
    write_json(
        storage,
        k_metrics,
        {
            "model_name": model_name,
            "run_id": run_id,
            "created_utc": run_id,
            "metrics": metrics,
        }
    )

    # preds
    storage.write_parquet(preds, k_preds, index=False)

    # latest pointer
    write_json(
        storage,
        k_latest,
        {
            "model_name": run_id,
            "updated_utc": run_id,
            "model_key": k_model,
            "metrics_key": k_metrics,
            "predictions_key": k_preds,
        }
    )

    return {
        "model_key": run_id,
        "metrics_key": k_metrics,
        "latest_key": k_latest,
        "predictions_key": k_preds,
    }