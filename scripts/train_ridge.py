"""
Train baseline ridge model and write canonical artifacts.

RESPONSIBILITIES:
- generate a unique run id (UTC)
- read model-ready dataset from storage
- train baseline model
- write model artifacts and eval (canonical)

OUTPUTS:
- artifacts/models/baseline/<run_id>/model.joblib
- artifacts/models/baseline/<run_id>/metrics.json
- artifacts/models/baseline/latest.json
- artifacts/eval/baseline/<run_id>/predictions.parquet
"""
from __future__ import annotations

from dotenv import load_dotenv

from src.pipelines.baseline import train_ridge
from src.storage.factory import get_storage
from src.storage.paths import utc_run_id, processed_merged
from src.materialization.model import write_model_artifacts

MODEL_NAME = "baseline"

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
    model, metrics, preds = train_ridge(merged)

    # write
    written = write_model_artifacts(
        storage=storage,
        model_name=MODEL_NAME,
        run_id=run_id,
        model=model,
        metrics=metrics,
        preds=preds,
        input_key=merged_key,
    )

    # Confirm
    INDENT = "    "
    print(INDENT)
    print(f"Run")
    print(f"{INDENT}ID:    {run_id}")
    print(f"{INDENT}Model: {MODEL_NAME}")
    print(f"{INDENT}RMSE:  {metrics['rmse']:.4f}")
    print(INDENT)
    print("Artifacts")
    print(f"{INDENT}model: {written['model_key']}")
    print(f"{INDENT}preds: {written['predictions_key']}")
    print(INDENT)


if __name__ == "__main__":
    main()