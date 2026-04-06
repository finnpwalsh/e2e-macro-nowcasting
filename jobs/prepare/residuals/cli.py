from __future__ import annotations

from typing import Any

from jobs._shared.cli import resolve_config
from .config import ResidualsConfig


def resolve_residuals_config() -> ResidualsConfig:
    return resolve_config(parse_residuals_config)


def parse_residuals_config(value: Any) -> ResidualsConfig:
    if not isinstance(value, dict):
        raise SystemExit("--config must deserialize to a JSON object.")
    
    run_family = value.get("run_family")
    if not isinstance(run_family, str):
        raise SystemExit("--config['policy'] must be a str.")

    target = value.get("target")
    if not isinstance(target, str):
        raise SystemExit("--config['target'] must be a str.")

    return ResidualsConfig(
        run_family=run_family,
        target=target,
    )