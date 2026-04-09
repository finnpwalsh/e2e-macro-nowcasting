
from __future__ import annotations

from typing import Protocol


class Storage(Protocol):
    """
    Abstract storage interface.
    """
    def read_bytes(self, key: str) -> bytes:
        ...
    
    def write_bytes(self, key: str, data: bytes) -> None:
        ...

    def exists(self, key: str) -> bool:
        ...
    
    def list(self, prefix: str) -> list[str]:
        ...