from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from macro_nowcast.interfaces import SourceDefinition
from .canonicalizers import ShockCanonicalizer, TiingoShockCanonicalizer
from macro_nowcast.storage import DATASETS


@dataclass(frozen=True)
class ShockSourceDefinition(SourceDefinition):
    canonicalizer: Type[ShockCanonicalizer]
    domain: str = "shocks"


SHOCK_SOURCES: dict[str, ShockSourceDefinition] = {
    "tiingo": ShockSourceDefinition(
        name="tiingo",
        canonicalizer=TiingoShockCanonicalizer,
        canonical_key=DATASETS.canonical.shocks_tiingo,
    ),
}