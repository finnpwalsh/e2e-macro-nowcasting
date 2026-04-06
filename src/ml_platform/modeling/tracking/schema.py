from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

from ml_platform.runs import RunArtifacts
from ml_platform.signatures import DataSignature, FeatureSignature
from ml_platform.storage.persistence import WriteOp


@dataclass(frozen=True)
class TrainingRunArtifacts:
    artifacts: RunArtifacts
    writes: Sequence[WriteOp]
    data_signature: DataSignature
    feature_signature: FeatureSignature