from __future__ import annotations

from typing import Protocol


class SecretResolver(Protocol):
    def get(self, name: str) -> str:
        ...