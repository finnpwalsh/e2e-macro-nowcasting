from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ..models import ModelSpec


@dataclass(frozen=True)
class SpecRegistry:
    specs: Mapping[str, ModelSpec]

    def get_spec(self, model: str) -> ModelSpec:
        try:
            return self.specs[model]
        except KeyError as e:
            available = ", ".join(sorted(self.specs))
            raise ValueError(
                f"Unknown model spec '{model}'. Available specs: {available}"
            ) from e


@dataclass(frozen=True)
class EngineRegistry:
    engines: Mapping[str, ModelSpec]

    def get_spec(self, engine: str, model: str) -> ModelSpec:
        try:
            spec_registry= self.engines[engine]
        except KeyError as e:
            available = ", ".join(sorted(self.engines))
            raise ValueError(
                f"Unknown engine '{engine}'. Available engines: {available}"
            ) from e
        
        return spec_registry.get_spec(model=model)


from .sklearn import SKLEARN

ENGINES = EngineRegistry(
    engines = {
        "sklearn": SKLEARN,
    }
)