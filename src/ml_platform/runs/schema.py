from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from ml_platform.storage.persistence import PersistencePlan
from ml_platform.signatures import DataSignature, FeatureSignature


@dataclass(frozen=True)
class RunManifest:
    run_family: str
    run_id: str
    created_at_utc: str

    input_key: str

    spec: Mapping[str, Any]
    provenance: Mapping[str, Any]

    data_signature: DataSignature
    feature_signature: FeatureSignature | None

    artifact_keys: Mapping[str, str]
    metrics: Mapping[str, Any]


@dataclass(frozen=True)
class RunSummary:
    run_family: str
    run_id: str
    created_at_utc: str

    input_key: str

    primary_metric: Mapping[str, Any] | None
    primary_artifact_key: str | None


@dataclass(frozen=True)
class RunPointer:
    run_family: str
    run_id: str
    
    manifest_key: str
    summary_key: str
    primary_artifact_key: str | None



@dataclass(frozen=True)
class TrackerResult:
    manifest: RunManifest
    summary: RunSummary
    persistence_plan: PersistencePlan