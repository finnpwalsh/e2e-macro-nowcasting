from __future__ import annotations

from ..registry import SpecRegistry
from .specs import RidgeSpec


SKLEARN = SpecRegistry(
    specs={
        "ridge": RidgeSpec(),
    }
)