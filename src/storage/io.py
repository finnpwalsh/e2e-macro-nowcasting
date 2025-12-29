from __future__ import annotations

import json
from typing import Any

import joblib

from src.storage.base import Storage

def write_json(storage: Storage, key: str, payload: dict) -> None:
    data = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    storage.write_bytes(data, key)

def read_json(storage: Storage, key: str) -> dict:
    data = storage.read_bytes(key)
    return json.loads(data.decode("utf-8"))

def write_joblib(storage: Storage, key: str, obj: Any) -> None:
    data = joblib.dump(obj)
    storage.write_bytes(data, key)

def read_joblib(storage: Storage, key: str) -> Any:
    data = storage.read_bytes(key)
    return joblib.load(data)