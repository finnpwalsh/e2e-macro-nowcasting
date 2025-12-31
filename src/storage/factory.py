"""
Storage factory.

Returns the appropriate Storage backend based on configuration.
"""

from __future__ import annotations

import os

from src.storage.base import Storage
from src.storage.local import LocalStorage
from src.storage.s3 import S3Storage


def get_storage() -> Storage:
    """
    Return a storage backend.

    Defaults to local filesystem storage.
    """

    backend = os.getenv("STORAGE_BACKEND", "local").lower()

    if backend == "local":
        return LocalStorage()

    elif backend == "s3":
        return S3Storage()
    
    raise ValueError(f"Unknown STORAGE_BACKEND: {backend}")