from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any
import json


@dataclass(frozen=True)
class TrainingRunConfig:
    run_family: str
    input_key: str
    target_col: str
    row_id_col: str | None = None
    extras: Mapping[str, str] | None = None


def parse_training_run_config(raw: str) -> TrainingRunConfig:
    try:
        value: Any = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"--run-config must be valid JSON: {e}") from e

    if not isinstance(value, dict):
        raise SystemExit("--run-config must deserialize to a JSON object.")

    run_family = value.get("run_family")
    if not isinstance(run_family, str) or not run_family.strip():
        raise SystemExit("--run-config['run_family'] must be a non-empty string.")

    input_key = value.get("input_key")
    if not isinstance(input_key, str) or not input_key.strip():
        raise SystemExit("--run-config['input_key'] must be a non-empty string.")

    target_col = value.get("target_col")
    if not isinstance(target_col, str) or not target_col.strip():
        raise SystemExit("--run-config['target_col'] must be a non-empty string.")

    row_id_col = value.get("row_id_col")
    if row_id_col is not None and not isinstance(row_id_col, str):
        raise SystemExit("--run-config['row_id_col'] must be a string or null.")

    params = value.get("params", {})
    if not isinstance(params, dict):
        raise SystemExit("--run-config['params'] must be an object.")

    return TrainingRunConfig(
        run_family=run_family.strip(),
        input_key=input_key.strip(),
        target_col=target_col.strip(),
        row_id_col=row_id_col,
        params=params,
    )