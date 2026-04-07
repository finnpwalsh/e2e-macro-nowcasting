from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ModelFamily(str, Enum):
    REGRESSION = "regression"
    CLASSIFICATION = "classification"


@dataclass(frozen=True)
class ModelDefinition:
    engine: str
    family: ModelFamily
    model: str
    params: dict

    def to_dict(self) -> dict:
        return {
            "engine": self.engine,
            "family": self.family,
            "model": self.model,
            "params": self.params,
        }