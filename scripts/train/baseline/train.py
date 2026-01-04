"""
Train baseline ridge model and materialize outputs.

RESPONSIBILITIES:
- generate a unique run id (UTC)
- read model-ready dataset from storage
- train baseline model
- write full eval preds to data storage(local/S3)
- log metrics + run metadata to MLflow
- log model to MLflow and register it
- update MLflow Registry alias (e.g. champion) to point to this version (latest)

OUTPUTS (Data store — local/S3):
- artifacts/eval/baseline/<run_id>/predictions.parquet
"""
from __future__ import annotations

import os
from dotenv import load_dotenv

from src.pipelines.baseline import train_ridge
from src.storage.factory import get_storage
from src.storage.paths import utc_run_id, processed_merged
from src.materialization.model import write_model_artifacts

def main() -> None:
    # load env
    load_dotenv()
    storage = get_storage()

    # get run id
    run_id = utc_run_id()

    # get merged
    merged_key = processed_merged()
    merged = storage.read_parquet(merged_key)

    # train
    model, metrics, preds, features = train_ridge(merged)

    # write
    written = write_model_artifacts(
        storage=storage,
        model_name="baseline",
        run_id=run_id,
        model=model,
        metrics=metrics,
        preds=preds,
        input_key=merged_key,
        features=features,
    )

    # Confirm
    INDENT = "    "
    print()
    print(f"Run")
    print(f"{INDENT}ID:          {run_id}")
    print(f"{INDENT}Mlflow run:  {written['mlflow_run_id']}")
    print(f"{INDENT}Experiment:  {os.getenv('MLFLOW_EXPERIMENT_NAME')}")
    print(f"{INDENT}Model:       {written['registry_model_name']}@{written['alias']}")
    print(f"{INDENT}Model URI:   {written['model_uri']}")
    print(f"{INDENT}RMSE:        {metrics['rmse']:.4f}")

    print()
    print("Outputs")
    print(f"{INDENT}preds key:   {written['predictions_key']}")
    print()


if __name__ == "__main__":
    main()