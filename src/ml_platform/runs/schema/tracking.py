from __future__ import annotations

from dataclasses import dataclass

from ml_platform.storage import PersistencePlan

from .summary import RunSummary
from .manifest import RunManifest


@dataclass(frozen=True)
class TrackerResult:
    manifest: RunManifest
    summary: RunSummary
    persistence_plan: PersistencePlan