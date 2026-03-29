from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any


@dataclass(frozen=True)
class RunSpec:
    engine: str
    name: str
    params: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "params": dict(self.params),
        }