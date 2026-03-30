from __future__ import annotations

import argparse

from ml_platform.modeling._core import (
    ModelDefinition,
    parse_model_definition,
    TrainingRunConfig,
    parse_training_run_config,
)


def parse_args() -> tuple[TrainingRunConfig, ModelDefinition]:
    parser = build_parser()
    args = parser.parse_args()

    model_def = parse_model_definition(args.model_def)
    run_config = parse_training_run_config(args.run_config)
    
    return run_config, model_def


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run model training job.")

    parser.add_argument("--model-definition", required=True)
    parser.add_argument("--run-config")

    return parser