from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

from ml_platform.storage import Storage, StorageIO, ParquetWrite, PersistencePlan, WriteOp
from ml_platform.runs import RunPointer, RunIdentity, PointerKeys
from ml_platform.modeling.core import PredictionsResolver

from .contract import ResidualsBuilder


@dataclass(frozen=True)
class ResidualsMaterializer:
    def build_plan(
        self,
        *,
        storage: Storage,
        run_family: str,
        target: str
    ) -> PersistencePlan:
        keys = PointerKeys(run_family=run_family)

        if target == "champion":
            ptr_key = keys.champion
        else:
            ptr_key = keys.latest
        
        ptr = RunPointer(**read_json(
            storage=storage,
            key=ptr_key
        ))

        run_identity = RunIdentity(**ptr.run_identity)

        keys = Keys(
            run_family=run_family,
            run_id = run_identity.run_id,
        )

        predictions = PredictionsResolver(storage).resolve(key=keys.datasets.predictions)
        residuals = ResidualsBuilder().build(predictions=predictions)
        
        writes: Sequence[WriteOp] = (
            ParquetWrite(
                key=keys.datasets.residuals,
                df=residuals.to_frame,
            ),
        )

        return PersistencePlan(writes=writes)