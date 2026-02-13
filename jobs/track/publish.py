"""
Track job: publish trained model artifacts to MLFlow.

Lifecycle stage:
    Track

Responsibilities:
    - Read the latest trained model manifest from storage
    - Load model artifacts, metrics, predictions, and run metadata
    - Log artifacts and metrics to the tracking backend (MLflow)
    - Register an immutable model version in the model registry

Inputs:
    - Latest model pointer metadata (model_latest)
    - Versioned model artifacts produced by Train

Outputs:
    - MLflow run with logged metrics and artifacts
    - Registered model version in the model registry

Out of scope:
    - Alias management or promotion
    - Model training or retraining
    - Mutation of training artifacts or metrics
    - Definition of artifact or storage layout
    - Online serving or inference

Notes:
    Tracking is best-effort and control-plane only. Training artifacts remain
    valid and usable even if tracking or registration fails. This job does not
    perform model selection beyond publishing the referenced run.
"""
from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage, read_joblib, read_json
from ml_platform.artifacts import ModelPointers
from ml_platform.mlflow.publish import log_and_register_model


def run(storage: Storage) -> None:
    """Publish the latest trained model artifacts to MLflow and register a versioned model."""
    model_name = "baseline"
    ptr = ModelPointers(model_name=model_name)
    
    latest = read_json(storage, ptr.latest)
    
    model = read_joblib(storage, latest["model_key"])
    metrics = read_json(storage, latest["metrics_key"])
    preds = storage.read_parquet(key=latest["predictions_key"])
    summary = read_json(storage, latest["summary_key"])
    
    run_id = latest["run_id"]
    features = summary["features"]
    input_key = summary["input_key"]
    predictions_key = latest["predictions_key"]

    written = log_and_register_model(
        model_name=model_name,
        run_id=run_id,
        model=model,
        metrics=metrics,
        preds=preds,
        features=features,
        input_key=input_key,
        predictions_key=predictions_key,
    )

    INDENT = "    "
    print("\n[TRACK][PUBLISH] Complete")
    print(f"{INDENT}Model:           {model_name}")
    print(f"{INDENT}MLflow Run ID:   {written['mlflow_run_id']}")
    print(f"{INDENT}Experiment ID:   {written['experiment_id']}")
    print(f"{INDENT}Registry Name:   {written['registry_model_name']}")
    print(f"{INDENT}Version:         {written['registry_model_version']}")
    print(f"{INDENT}Model URI:       {written['model_uri']}")
    print(f"{INDENT}Predictions Key: {written['predictions_key']}")


def main() -> None:
    load_dotenv()
    run(get_storage())


if __name__ == "__main__":
    main()