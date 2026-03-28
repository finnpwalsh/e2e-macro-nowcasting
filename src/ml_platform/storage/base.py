"""
Storage interface definition.

Defines the contract that all storage backends (local
filesystem, S3, etc.) must implement.

This file contains no implementation logic.
"""
from __future__ import annotations

from typing import Protocol
import pandas as pd


class Storage(Protocol):
    """
    Abstract storage interface.

    All paths are expressed as string keys (e.g.: 
    'data/raw/fred/fred_all.parquet').

    Implementations decide how and where data is stored.
    """

    def read_parquet(self, key: str) -> pd.DataFrame:
        """Read a parquet object from storage."""
        ...
    
    def write_parquet(self, key: str, df: pd.DataFrame, **kwargs) -> None:
        """Write a DataFrame to storage as parquet."""
        ...
    
    def read_bytes(self, key: str) -> bytes:
        """Read raw bytes from storage."""
        ...
    
    def write_bytes(self, key: str, data: bytes) -> None:
        """Write raw bytes to storage."""
        ...

    def exists(self, key: str) -> bool:
        """Check whether a key exists in storage."""
        ...