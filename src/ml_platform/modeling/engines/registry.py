from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ml_platform.modeling._core import ModelSpec

from .sklearn import SKLEARN_SPECS


@dataclass(frozen=True)
class SpecRegistry:
    specs: dict[str, ModelSpec]

    def get(self, name: str) -> ModelSpec:
        try:
            return self.specs[name]
        except KeyError as e:
            available = ", ".join(sorted(self.specs))
            raise ValueError(
                f"Unknown model spec '{name}'. Available specs: {available}"
            ) from e


@dataclass(frozen=True)
class EngineRegistry:
    engines: Mapping[str, SpecRegistry]

    def get(self, name: str) -> SpecRegistry:
        try:
            return self.engines[name]
        except KeyError as e:
            available = ", ".join(sorted(self.engines))
            raise ValueError(
                f"Unknown engine '{name}'. Available engines: {available}"
            ) from e

ENGINES = EngineRegistry(
    engines = {
        "sklearn": SKLEARN_SPECS,
    }
)