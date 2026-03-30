from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any


@dataclass(frozen=True)
class ModelDefinition:
    engine: str
    name: str
    params: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine": self.name,
            "name": self.name,
            "params": dict(self.params),
        }