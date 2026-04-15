from __future__ import annotations

from collections.abc import Sequence

from ml_platform.platform.persistence import PersistencePlan, WriteOp, JsonWrite
from ml_platform.platform.contracts import DataSignature
from ml_platform.platform.runs import RunIdentity
from ml_platform.modeling.features import FeatureSignature
from ml_platform.modeling.outputs import Predictions
from ml_platform.modeling.training import TrainedModel

from ..persistence import ParquetWrite, JoblibWrite

from .schema import (
    TrainingRunRefs,
    TrainingRunSpec,
    TrainingRunOutputs,
    TrainingSummary,
    TrainingRunSummary,
    TrainingRunManifest,
)
from .keys import TrainingRunKeys

class TrainingTrackingService:
    def build_plan(
        run_identity: RunIdentity,
        refs: TrainingRunRefs,
        spec: TrainingRunSpec,
        outputs: TrainingRunOutputs,
        t_summary: TrainingSummary,
        trained_model: TrainedModel,
        predictions: Predictions,
        data_signature: DataSignature,
        feature_signature: FeatureSignature | None = None,
    ) -> PersistencePlan:
        keys = TrainingRunKeys(
            run_family=run_identity.run_family,
            run_id=run_identity.run_id,
        )

        manifest = TrainingRunManifest(
            run_identity=run_identity,
            refs=refs,
            spec=spec,
            outputs=outputs,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )

        summary = TrainingRunSummary(
            run_identity=run_identity,
            refs=refs,
            summary=t_summary,
        )

        writes: Sequence[WriteOp] = (
            JsonWrite(
                key=keys.manifest,
                payload=manifest,
            ),
            JsonWrite(
                key=keys.summary,
                payload=summary,
            ),
            ParquetWrite(
                key=keys.predictions,
                df=predictions.to_frame,
            ),
            JoblibWrite(
                key=keys.model,
            ),
        )

        return PersistencePlan(writes)