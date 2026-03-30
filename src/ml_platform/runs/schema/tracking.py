from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from collections.abc import Sequence

import pandas as pd

from ml_platform.modeling._core import Metrics
from ml_platform.storage.persistence import WriteOp, PersistencePlan

from ml_platform.runs import RunContext

from .spec import RunSpec
from .artifacts import RunArtifacts
from .summary import RunSummary
from .manifest import RunManifest


@dataclass(frozen=True)
class TrackingInput:
    ctx: RunContext
    input_key: str
    spec: RunSpec
    metrics: Metrics

    full_df: pd.DataFrame
    train_df: pd.DataFrame | None = None
    valid_df: pd.DataFrame | None = None
    feature_cols: Sequence[str] | None = None

    artifacts: RunArtifacts
    artifact_writes: Sequence[WriteOp] = ()
    run_config: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class TrackerResult:
    manifest: RunManifest
    summary: RunSummary
    persistence_plan: PersistencePlan