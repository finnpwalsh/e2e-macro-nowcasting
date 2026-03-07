from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class RunManifest:
    model_name: str
    run_id: str
    created_at_utc: str

    input_key: str
    split_date: str

    spec: Mapping[str, Any]
    provenance: Mapping[str, Any]

    data_signature: Mapping[str, Any]
    feature_signature: Mapping[str, Any]

    artifacts: Mapping[str, Any]
    metrics: Mapping[str, Any]


@dataclass(frozen=True)
class RunSummary:
    model_name: str
    run_id: str
    created_at_utc: str

    input_key: str
    split_date: str

    primary_metric: Mapping[str, float]
    model_artifact_key: str


@dataclass(frozen=True)
class LatestPointer:
    model_name: str
    run_id: str
    manifest_key: str
    model_artifact_key: str