from dataclasses import dataclass, asdict, is_dataclass
from typing import Any, Mapping

import pandas as pd

from ml_platform.storage import Storage
from ml_platform.storage.serde import write_joblib, write_json


# -------------------------------------------
# Artifact classes
# -------------------------------------------

@dataclass(frozen=True)
class JsonArtifact:
    key: str
    payload: Any


@dataclass(frozen=True)
class JoblibArtifact:
    key: str
    obj: Any

@dataclass(frozen=True)
class ParquetArtifact:
    key: str
    df: pd.DataFrame

# -------------------------------------------
# Persistence plan
# -------------------------------------------

Artifact = JsonArtifact | JoblibArtifact | ParquetArtifact

@dataclass(frozen=True)
class PersistencePlan:
    artifacts: list[Artifact]

    def persist(self, *, storage: Storage) -> None:
        for artifact in self.artifacts:
            if isinstance(artifact, ParquetArtifact):
                storage.write_parquet(key=artifact.key, df=artifact.df)
            elif isinstance(artifact, JoblibArtifact):
                write_joblib(storage=storage, key=artifact.key, obj=artifact.obj)
            elif isinstance(artifact, JsonArtifact):
                write_json(
                    storage=storage,
                    key=artifact.key,
                    payload=self._resolve_json_payload(artifact.payload),
                )
        
    @staticmethod
    def _resolve_json_payload(payload: Any) -> Any:
        if is_dataclass(payload):
            return asdict(payload)
        elif isinstance(payload, Mapping):
            return dict(payload)
        else:
            raise TypeError(
                f"JsonArtifact payload must be a dataclass or mapping, got {type(payload).__name__}"
            )