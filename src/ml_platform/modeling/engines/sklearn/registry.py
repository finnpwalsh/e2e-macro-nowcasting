from __future__ import annotations

from ml_platform.modeling.regression.engines import SpecRegistry
from .specs import RidgeSpec


SKLEARN_SPECS = SpecRegistry(
    specs={
        "ridge": RidgeSpec(),
    }
)