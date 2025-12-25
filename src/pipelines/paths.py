from __future__ import annotations

from pathlib import Path
from src.config.paths import ARTIFACTS_DIR

def get_run_dir(run_id: str) -> Path:
    """
    Return run-scoped directory.
    """
    return (ARTIFACTS_DIR / run_id)

def get_artifact_dirs(run_id: str) -> tuple[Path, Path, Path]:
    """
    Return run-scoped artifact directories.

    Order:
        (run_dir, models_dir, metrics_dir, preds_dir)
    """
    run_dir = get_run_dir(run_id)
    return (
        run_dir / "models",
        run_dir / "metrics",
        run_dir / "predictions",
    )