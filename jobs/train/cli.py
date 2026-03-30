from __future__ import annotations

import json
import argparse

from typing import Any

from ml_platform.modeling._core import ModelDefinition
from .config import TrainingRunConfig


def parse_model_definition(raw: str) -> ModelDefinition:
    try:
        value = json.loads(raw)
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


def parse_string_mapping(raw: str) -> dict[str, str]:
    try:
        value: Any = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"--extras must be valid JSON: {e}") from e

    if not isinstance(value, dict):
        raise SystemExit("--extras must deserialize to a JSON object.")

    out: dict[str, str] = {}
    for k, v in value.items():
        if not isinstance(k, str):
            raise SystemExit("--extras keys must all be strings.")
        if not isinstance(v, str):
            raise SystemExit("--extras values must all be strings.")
        out[k] = v

    return out



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run model training job.")

    parser.add_argument("--model-def", required=True)
    parser.add_argument("--run-family", required=True)
    parser.add_argument("--input-key", required=True)
    parser.add_argument("--target-col", required=True)
    parser.add_argument("--row-id-col", required=False, default=None)
    parser.add_argument(
        "--extras",
        required=False,
        default=None,
        help='JSON object, e.g. \'{"time_col":"ds","split_date":"2020-01-01"}\'',
    )

    return parser


def parse_args() -> tuple[TrainingRunConfig, ModelDefinition]:
    parser = build_parser()
    args = parser.parse_args()

    extras = parse_string_mapping(args.extras) if args.extras is not None else None

    run_config = TrainingRunConfig(
        run_family=args.run_family,
        input_key=args.input_key,
        target_col=args.target_col,
        row_id_col=args.row_id_col,
        primary_metric=args.primary_metric,
        extras=extras,
    )

    model_def = parse_model_definition(args.model_def)
    return run_config, model_def