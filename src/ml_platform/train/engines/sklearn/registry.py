from __future__ import annotations

from dataclasses import dataclass

from .specs import SklearnModelSpec, RidgeSpec


SKLEARN_MODEL_SPECS: dict[str, SklearnModelSpec] = {
    "ridge": RidgeSpec(),
}