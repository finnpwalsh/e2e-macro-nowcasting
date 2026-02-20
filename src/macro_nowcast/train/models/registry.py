from __future__ import annotations

from dataclasses import dataclass

from .base import ModelSpec
from .ridge import RidgeModelSpec


@dataclass(frozen=True)
class ModelSpecDefinition:
    name: str
    spec: ModelSpec


MODELS: dict[str, ModelSpecDefinition] = {
    "ridge": ModelSpecDefinition(
        name="ridge",
        spec=RidgeModelSpec,
    )
}