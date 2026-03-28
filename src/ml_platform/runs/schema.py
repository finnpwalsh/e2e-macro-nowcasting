from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from ml_platform.storage.persistence import PersistencePlan
from ml_platform.signatures import DataSignature, FeatureSignature
from ml_platform.evaluation import Metric, Metrics


@dataclass(frozen=True)
class RunIdentity:
    run_family: str
    run_id: str
    created_at_utc: str

    def to_dict(self) -> dict[str, str]:
        return {
            "run_family": self.run_family,
            "run_id": self.run_id,
            "created_at_utc": self.created_at_utc,
        }


@dataclass(frozen=True)
class RunSpec:
    name: str
    params: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "params": dict(self.params),
        }


@dataclass(frozen=True)
class RunArtifacts:
    primary: str | None = None
    extras: Mapping[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, str]:
        out: dict[str, str] = {}

        if self.primary is not None:
            out["primary"] = self.primary
        
        out.update(dict(self.extras))
        return out


@dataclass(frozen=True)
class RunManifest:
    run_identity: RunIdentity
    input_key: str
    spec: RunSpec
    artifact_keys: ArtifactKeys
    metrics: Metrics
    data_signature: DataSignature
    feature_signature: FeatureSignature | None


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