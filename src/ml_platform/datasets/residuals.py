from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

from ml_platform.storage import Storage, PointerKeys, Keys
from ml_platform.storage.persistence import ParquetWrite, PersistencePlan, WriteOp
from ml_platform.storage.serde import read_json
from ml_platform.runs.schema import RunPointer, RunIdentity
from ml_platform.modeling._core import PredictionsResolver
from ml_platform.modeling.regression import ResidualsBuilder


@dataclass(frozen=True)
class ResidualsService:
    def run(
        self,
        *,
        storage: Storage,
        run_family: str,
        target: str
    ) -> None:
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

        PersistencePlan(writes=writes).persist(storage=storage)