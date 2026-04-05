from __future__ import annotations

from typing import Any

from .config import (
    SelectionConfig,
    SelectionPolicyConfig,
    SelectionTargetConfig,
)

from jobs._shared.cli import resolve_config


def resolve_selection_config() -> SelectionConfig:
    return resolve_config(parse_selection_config)


def parse_selection_config(value: Any) -> SelectionConfig:
    if not isinstance(value, dict):
        raise SystemExit("--select-config must deserialize to a JSON object.")

    target_raw = value.get("target")
    if not isinstance(target_raw, dict):
        raise SystemExit("--select-config['target'] must be an object.")

    policy_raw = value.get("policy")
    if not isinstance(policy_raw, dict):
        raise SystemExit("--select-config['policy'] must be an object.")

    target = _parse_target_config(target_raw)
    policy = _parse_policy_config(policy_raw)

    return SelectionConfig(
        target=target,
        policy=policy,
    )


def _parse_target_config(target: dict) -> SelectionTargetConfig:
    model_family = target.get("model_family")
    
    if not isinstance(model_family, str) or not model_family.strip():
        raise SystemExit("--select-config['target']['model_family'] must be a non-empty string.")
    
    return SelectionTargetConfig(model_family)


def _parse_policy_config(policy: dict) -> SelectionPolicyConfig:
    primary_metric = policy.get("primary_metric")
    if not isinstance(primary_metric, str) or not primary_metric.strip():
        raise SystemExit("--select-config['policy']['primary_metric'] must be a non-empty string.")

    minimum_proportional_improvement = policy.get("minimum_proportional_improvement", 0.0)
    if not isinstance(minimum_proportional_improvement, (float)):
        raise SystemExit(
            "--select-config['policy']['minimum_proportional_improvement'] must be a float."
        )
    
    if minimum_proportional_improvement < 0.0:
        raise SystemExit(
            "--select-config['policy']['minimum_relative_improvement'] must be >= 0.0."
        )
    
    return SelectionPolicyConfig(
        primary_metric=primary_metric,
        minimum_proportional_improvement=minimum_proportional_improvement,
    )