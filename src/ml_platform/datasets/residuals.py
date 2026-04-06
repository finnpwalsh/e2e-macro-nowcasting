from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

from ml_platform.storage import Storage, PointerKeys, Keys
from ml_platform.storage.persistence import ParquetWrite, PersistencePlan, WriteOp
from ml_platform.storage.serde import read_json
from ml_platform.runs.schema import RunPointer, RunManifest
from ml_platform.modeling._core import Predictions
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

        manifest = RunManifest(**read_json(
            storage=storage,
            key=ptr.manifest_key,
        ))

        predictions = Predictions(**storage.read_parquet(key=manifest.artifacts["predictions"]))

        residuals = ResidualsBuilder().build(predictions=predictions)

        keys = Keys(
            run_family=run_family,
            run_id = ptr.run_identity.run_id,
        )
        
        writes: Sequence[WriteOp] = (
            ParquetWrite(
                key=keys.datasets.residuals,
                df=residuals.to_frame(),
            ),
        )

        PersistencePlan(writes).persist(storage)