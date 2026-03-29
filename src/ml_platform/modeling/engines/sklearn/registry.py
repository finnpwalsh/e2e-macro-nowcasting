from __future__ import annotations

from ml_platform.modeling.engines import SpecRegistry
from .specs import RidgeSpec


SKLEARN = SpecRegistry(
    specs={
        "ridge": RidgeSpec(),
    }
)