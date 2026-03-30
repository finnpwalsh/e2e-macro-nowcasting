from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any

from ml_platform.signatures import DataSignature, FeatureSignature
from ml_platform.modeling._core import Metrics

from .artifacts import RunArtifacts
from .identity import RunIdentity


@dataclass(frozen=True)
class RunManifest:
    run_identity: RunIdentity
    input_key: str
    spec: Mapping[str, Any]
    artifacts: RunArtifacts
    metrics: Metrics
    data_signature: DataSignature
    feature_signature: FeatureSignature | None