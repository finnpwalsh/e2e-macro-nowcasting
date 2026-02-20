from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage, write_joblib, write_json
from ml_platform.artifacts import TrainArtifacts, EvalArtifacts, ModelPointers, new_run_id
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.train.baseline import BaselineCandidateGenerator
from macro_nowcast.train.models import MODELS

MODEL_NAME = "baseline"
TARGET_COL = "cpi_all_items"
TIME_COL = "ds"

SPLIT_DATE = "2020-01-01"
ALPHA = 1.0


def run(storage: Storage) -> None:
    run_id = new_run_id()

    tr = TrainArtifacts(model_name=MODEL_NAME, run_id=run_id)
    ev = EvalArtifacts(model_name=MODEL_NAME, run_id=run_id)
    ptr = ModelPointers(model_name=MODEL_NAME)

    in_key = DATASETS.model_ready.anchors
    df = storage.read_parquet(key=in_key)

    gen = BaselineCandidateGenerator(
        model_name=MODEL_NAME,
        time_col=TIME_COL,
        target_col=TARGET_COL,
        SPLIT_DATE=SPLIT_DATE,
    )

    out = gen.generate(df=df, spec=MODELS["ridge"].spec)
    
    write_joblib(storage, key=tr.model, obj=out.model)
    write_json(storage, key=tr.metrics, obj=out.metrics)
    storage.write_parquet(key=ev.predictions, df=out.predictions)
    write_json(storage, key=ev.summary, payload=out.summary)

    # pointer
    write_json(
        storage,
        key=ptr.latest,
        payload={
            "model_name": MODEL_NAME,
            "run_id": run_id,
            "input_key": in_key,
            "model_key": tr.model,
            "metrics_key": tr.metrics,
            "predictions_key": ev.predictions,
            "summary_key": ev.summary,
        },
    )
    

    INDENT = "    "
    print("\n[Train][BASELINE] Complete")
    print(f"{INDENT}model:       {MODEL_NAME}")
    print(f"{INDENT}run id:      {run_id}")
    print(f"{INDENT}input:       {in_key}")
    print(f"{INDENT}latest:      {ptr.latest}")


def main() -> None:
    load_dotenv()
    run(get_storage())


if __name__ == "__main__":
    main()