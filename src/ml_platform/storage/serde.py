from __future__ import annotations

import json
from typing import Any
from io import BytesIO

from .base import Storage


def write_json(storage: Storage, key: str, payload: dict) -> None:
    data = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    storage.write_bytes(key=key, data=data)

def read_json(storage: Storage, key: str) -> dict:
    data = storage.read_bytes(key=key)
    return json.loads(data.decode("utf-8"))

def write_joblib(storage: Storage, key: str, obj: Any) -> None:
    import joblib
    buffer = BytesIO()
    joblib.dump(obj, buffer)
    buffer.seek(0)
    storage.write_bytes(key=key, data=buffer.read())

def read_joblib(storage: Storage, key: str) -> Any:
    import joblib
    data = storage.read_bytes(key=key)
    buffer = BytesIO(data)
    return joblib.load(buffer)