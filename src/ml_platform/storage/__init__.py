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

__all__ = [
    "Storage",
    "get_storage",
]