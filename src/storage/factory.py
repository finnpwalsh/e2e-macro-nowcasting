"""
Storage factory.

Returns the appropriate Storage backend based on configuration.
"""

from __future__ import annotations

import os

from src.storage.base import Storage
from src.storage.local import LocalStorage


def get_storage() -> Storage:
    """
    Return a storage backend.

    Defaults to local filesystem storage.
    """

    backend = os.getenv("STORAGE_BACKEND", "local").lower()

    if backend == "local":
        return LocalStorage()

    elif backend == "s3":
        raise NotImplementedError("S3 storage backend not implemented yet.")
    
    else:
        raise ValueError(f"Unknown STORAGE_BACKEND: {backend}")