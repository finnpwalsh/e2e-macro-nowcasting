from __future__ import annotations

from pathlib import Path

ARTIFACTS_ROOT = Path("artifacts")

def run_dir(run_id: str) -> Path:
    """
    Return the root artifact directory for a given run.
    """
    return ARTIFACTS_ROOT / run_id

def model_path(run_id: str) -> Path:
    return run_dir(run_id) / "models"

def metrics_path(run_id: str) -> Path:
    return run_dir(run_id) / "metrics"

def preds_path(run_id: str) -> Path:
    return run_dir(run_id) / "predictions"

def latest_run_id() -> str | None:
    runs = [p.name for p in ARTIFACTS_ROOT.iterdir() if p.is_dir()]
    return max(runs) if runs else None