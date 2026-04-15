from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .canonicalizer import Canonicalizer


D = TypeVar("D")


@dataclass(frozen=True)
class SourceDefinition(Generic[D]):
    """
    Registry-level definition of a data source.

    Binds:
        - source identity
        - logical domain
        - canonicalizer implementation
        - canonical dataset storage key
    """
    name: str
    canonicalizer_cls: type[Canonicalizer[D]]
    canonical_key: str
    domain: D