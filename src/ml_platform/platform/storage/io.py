from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from io import BytesIO
import json

from .base import Storage


@dataclass(frozen=True)
class StorageIO:
    storage: Storage

    # --------- JSON ---------
    def write_json(self, *, key: str, payload: dict) -> None:
        data = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.storage.write_bytes(key=key, data=data)

    def read_json(self, *, key: str) -> dict:
        data = self.storage.read_bytes(key=key)
        return json.loads(data.decode("utf-8"))

    # --------- Joblib ---------
    def write_joblib(self, *, key: str, obj: Any) -> None:
        import joblib
        buffer = BytesIO()
        joblib.dump(obj, buffer)
        buffer.seek(0)
        self.storage.write_bytes(key=key, data=buffer.read())

    def read_joblib(self, *, key: str) -> Any:
        import joblib
        data = self.storage.read_bytes(key=key)
        buffer = BytesIO(data)
        return joblib.load(buffer)