"""
Registry-level definition of a data source.

Binds:
    - Provider identity (name)
    - Domain ("anchors" or "shocks")
    - Canonicalizer class
    - Canonical dataset storage key
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Type

from .canonicalizer import Canonicalizer

Domain = Literal["anchors", "shocks"]


@dataclass(frozen=True)
class SourceDefinition:
    name: str
    canonicalizer: Type[Canonicalizer]
    canonical_key: str
    domain: Domain