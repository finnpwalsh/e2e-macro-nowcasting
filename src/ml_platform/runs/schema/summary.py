from __future__ import annotations

from dataclasses import dataclass

from ml_platform.storage.persistence import PersistencePlan
from ml_platform.modeling._core import Metric

from .identity import RunIdentity
from .manifest import RunManifest


@dataclass(frozen=True)
class RunSummary:
    run_identity: RunIdentity
    input_key: str
    primary_metric: Metric | None
    primary_artifact_key: str | None


@dataclass(frozen=True)
class RunPointer:
    run_identity: RunIdentity
    manifest_key: str
    summary_key: str
    primary_artifact_key: str | None


@dataclass(frozen=True)
class TrackerResult:
    manifest: RunManifest
    summary: RunSummary
    persistence_plan: PersistencePlan