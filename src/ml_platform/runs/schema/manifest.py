from __future__ import annotations

from dataclasses import dataclass

from ml_platform.signatures import DataSignature, FeatureSignature
from ml_platform.modeling._core import Metrics

from .artifacts import RunArtifacts
from .identity import RunIdentity
from .spec import RunSpec


@dataclass(frozen=True)
class RunManifest:
    run_identity: RunIdentity
    input_key: str
    spec: RunSpec
    artifacts: RunArtifacts
    metrics: Metrics
    data_signature: DataSignature
    feature_signature: FeatureSignature | None