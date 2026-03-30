from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .identity import RunIdentity


@dataclass(frozen=True)
class RunSummary:
    run_identity: RunIdentity
    input_key: str
    primary_artifact_key: str | None
    metrics: Mapping[str, float]


@dataclass(frozen=True)
class RunPointer:
    run_identity: RunIdentity
    manifest_key: str
    summary_key: str
    primary_artifact_key: str | None