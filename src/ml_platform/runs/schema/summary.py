from __future__ import annotations

from dataclasses import dataclass

from .identity import RunIdentity
from ml_platform.modeling._core import Metrics


@dataclass(frozen=True)
class RunSummary:
    run_identity: RunIdentity
    input_key: str
    primary_artifact_key: str | None
    metrics: Metrics


@dataclass(frozen=True)
class RunPointer:
    run_identity: RunIdentity
    manifest_key: str
    summary_key: str
    primary_artifact_key: str | None


@dataclass(frozen=True)
class ResolvedRun:
    pointer: RunPointer
    summary: RunSummary