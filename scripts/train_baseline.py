from __future__ import annotations

import json
from pathlib import Path

import joblib

from src.pipelines.train_baseline import train_ridge

OUTDIR = Path("artifacts")

OUT_MOD = OUTDIR / "models"
OUT_MET = OUTDIR / "metrics"
OUT_PRED = OUTDIR / "predictions"

def main() -> None:
    model, metrics, preds = train_ridge()
    
    # reproducibility
    OUT_MOD.mkdir(parents=True, exist_ok=True)
    OUT_MET.mkdir(parents=True, exist_ok=True)
    OUT_PRED.mkdir(parents=True, exist_ok=True)


    # save model
    joblib.dump(model, OUT_MOD / "baseline_ridge.joblib")

    # save metrics
    (OUT_MET / "baseline_ridge.json").write_text(
        json.dumps(metrics, indent=2)
    )

    # save preds (plotting + EDA)
    preds.to_parquet(OUT_PRED / "baseline_ridge.parquet", index=False)

    # output
    print(f"Baseline ridge RMSE: {metrics['rmse']:.4f}")
    print("Saved:", OUT_MOD / "baseline_ridge.joblib")
    print("Saved:", OUT_MET / "baseline_ridge.json")
    print("Saved:", OUT_PRED / "baseline_ridge.parquet")


if __name__ == "__main__":
    main()