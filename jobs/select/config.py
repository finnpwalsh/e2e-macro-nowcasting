from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SelectionTargetConfig:
    run_family: str


@dataclass(frozen=True)
class SelectionPolicyConfig:
    primary_metric: str
    minimum_relative_improvement: float


@dataclass(frozen=True)
class SelectionConfig:
    target: SelectionTargetConfig
    policy: SelectionPolicyConfig