from __future__ import annotations

from typing import Any
import json, argparse

from ml_platform.modeling._core import ModelDefinition

from .config import TrainingRunConfig


def parse_args() -> tuple[TrainingRunConfig, ModelDefinition]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--run-config",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--model-def",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    run_config = parse_training_run_config(args.run_config)
    model_definition = parse_model_definition(args.model_def)

    return run_config, model_definition


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


def parse_model_definition(raw: str) -> ModelDefinition:
    try:
        value: Any = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"--model-def must be valid JSON: {e}") from e

    if not isinstance(value, dict):
        raise SystemExit("--model-def must deserialize to a JSON object.")

    engine = value.get("engine")
    if not isinstance(engine, str) or not engine.strip():
        raise SystemExit("--model-def['engine'] must be a non-empty string.")

    model = value.get("model")
    if not isinstance(model, str) or not model.strip():
        raise SystemExit("--model-def['model'] must be a non-empty string.")

    params = value.get("params", {})
    if not isinstance(params, dict):
        raise SystemExit("--model-def['params'] must be an object.")

    return ModelDefinition(
        engine=engine.strip(),
        name=model.strip(),
        params=params,
    )