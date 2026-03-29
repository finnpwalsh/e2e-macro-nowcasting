from __future__ import annotations

import argparse
import json

from ml_platform.runs import RunSpec
from ml_platform.modeling.time_series import TimeSeriesTrainingConfig

from .config import TrainingRunConfig


def _parse_spec(raw: str) -> RunSpec:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"--spec must be valid JSON: {e}") from e

    if not isinstance(value, dict):
        raise SystemExit("--spec must deserialize to a JSON object.")
    
    engine = value.get("engine")
    if not isinstance(model, str) or not model.strip():
        raise SystemExit("--spec['engine'] must be a non-empty string.")

    model = value.get("model")
    if not isinstance(model, str) or not model.strip():
        raise SystemExit("--spec['model'] must be a non-empty string.")

    params = value.get("params", {})
    if not isinstance(params, dict):
        raise SystemExit("--spec['params'] must be an object.")

    return RunSpec(
        engine=engine,
        name=model,
        params=params,
    )


def parse_args() -> tuple[TrainingRunConfig, TimeSeriesTrainingConfig]:
    parser = argparse.ArgumentParser(description="Run model training job.")

    parser.add_argument("--run-family", required=True)
    parser.add_argument("--input-key", required=True)
    parser.add_argument("--time-col", required=True)
    parser.add_argument("--target-col", required=True)
    parser.add_argument("--split-date", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--primary-metric", required=True)

    args = parser.parse_args()

    run_config = TrainingRunConfig(
        run_family=args.run_family,
        input_key=args.input_key,
    )

    training_config = TimeSeriesTrainingConfig(
        time_col=args.time_col,
        target_col=args.target_col,
        split_date=args.split_date,
        spec=_parse_spec(args.spec),
        primary_metric=args.primary_metric,
    )

    return run_config, training_config