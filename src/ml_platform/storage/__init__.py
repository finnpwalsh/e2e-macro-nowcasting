"""
Storage layer.

Responsibilities:
    - Define the Storage interface (ADT)
    - Provide backend selection (local, S3)
    - Provide serialization helpers (JSON, joblib)

Artifact layout and lifecycle semantics live in `ml_platform.artifacts`
"""
from .base import Storage
from .factory import get_storage

from .serde import (
    read_json,
    write_json,
    read_joblib,
    write_joblib,
)

__all__ = [
    # Interface
    "Storage",

    # Backend factory
    "get_storage",

    # Serde helpers
    "read_json",
    "write_json",
    "read_joblib",
    "write_joblib",
]