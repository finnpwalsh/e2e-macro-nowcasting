from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .config import RunConfig, SplitConfig, TrainingConfig
from ml_platform.modeling._core import ModelDefinition


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        required=True,
    )

    return parser


def parse_args() -> argparse.Namespace:
    return build_parser().parse_args()


def load_training_config(path: str) -> TrainingConfig:
    config_path = Path(path)

    if not config_path.exists():
        raise SystemExit(f"--config file does not exist: {config_path}")
    
    if not config_path.is_file():
        raise SystemExit(f"--config must point to a file: {config_path}")
    
    try:
        raw = config_path.read_text(encoding="utf-8")
    except OSError as e:
        raise SystemExit(f"Failed to read config file '{config_path}': {e}") from e
    
    try:
        value: Any = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Config file '{config_path}' must contain valid JSON: {e}")
    
    return parse_training_config_dict(value)


def parse_training_config_dict(value: Any) -> TrainingConfig:
    if not isinstance(value, dict):
        raise SystemExit("Training config must deserialize to a JSON object.")
    
    run_value = value.get("run")
    if not isinstance(run_value, dict):
        raise SystemExit("config['run'] must be an object.")
    
    split_value = value.get("split")
    if not isinstance(split_value, dict):
        raise SystemExit("config['split'] must be an object.")
    
    model_value = value.get("model")
    if not isinstance(model_value, dict):
        raise SystemExit("config['model'] must be an object.")
    
    run = parse_run_config(run_value)
    split = parse_split_config(split_value)
    model = parse_model_definition(model_value)

    return TrainingConfig(
        run=run,
        split=split,
        model=model,
    )


def parse_run_config(value: dict[str, Any]) -> RunConfig:
    run_family = value.get("run_family")
    if not isinstance(run_family, str) or not run_family.strip():
        raise SystemExit("config['run']['run_family'] must be a non-empty string.")

    input_key = value.get("input_key")
    if not isinstance(input_key, str) or not input_key.strip():
        raise SystemExit("config['run']['input_key'] must be a non-empty string.")

    target_col = value.get("target_col")
    if not isinstance(target_col, str) or not target_col.strip():
        raise SystemExit("config['run']['target_col'] must be a non-empty string.")

    row_id_col = value.get("row_id_col")
    if row_id_col is not None and (not isinstance(row_id_col, str) or not row_id_col.strip()):
        raise SystemExit("config['run']['row_id_col'] must be null or a non-empty string.")

    return RunConfig(
        run_family=run_family,
        input_key=input_key,
        target_col=target_col,
        row_id_col=row_id_col,
    )


def parse_split_config(value: dict[str, Any]) -> SplitConfig:
    split_type = value.get("type")
    if not split_type == "time":
        raise SystemExit("config['split']['type'] must be 'time'.")

    time_col = value.get("time_col")
    if not isinstance(time_col, str) or not time_col.strip():
        raise SystemExit(
            "config['split']['time_col'] must be a non-empty string when split.type='time'."
        )

    split_date = value.get("split_date")
    if not isinstance(split_date, str) or not split_date.strip():
        raise SystemExit(
            "config['split']['split_date'] must be a non-empty string when split.type='time'."
        )

    return SplitConfig(
        type=split_type,
        time_col=time_col,
        split_date=split_date,
    )


def parse_model_definition(value: dict[str, Any]) -> ModelDefinition:
    engine = value.get("engine")
    if not isinstance(engine, str) or not engine.strip():
        raise SystemExit("config['model']['engine'] must be a non-empty string.")

    model_name = value.get("model")
    if not isinstance(model_name, str) or not model_name.strip():
        raise SystemExit("config['model']['model'] must be a non-empty string.")

    params = value.get("params", {})
    if not isinstance(params, dict):
        raise SystemExit("config['model']['params'] must be an object.")

    return ModelDefinition(
        engine=engine,
        name=model_name,
        params=params,
    )