from __future__ import annotations

from dataclasses import dataclass

from .specs import SklearnModelSpec, RidgeSpec


@dataclass(frozen=True)
class ModelSpecDefinition:
    name: str
    spec: SklearnModelSpec


MODELS: dict[str, ModelSpecDefinition] = {
    "ridge": ModelSpecDefinition(
        name="ridge",
        spec=RidgeSpec(),
    )
}