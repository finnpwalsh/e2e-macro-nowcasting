from __future__ import annotations

from dataclasses import dataclass

from ml_platform.train.components import ModelSpec
from .ridge import SKRidgeModelSpec


@dataclass(frozen=True)
class ModelSpecDefinition:
    name: str
    spec: ModelSpec


MODELS: dict[str, ModelSpecDefinition] = {
    "ridge": ModelSpecDefinition(
        name="ridge",
        spec=SKRidgeModelSpec(),
    )
}