from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .canonicalizers.tiingo import TiingoShockCanonicalizer
from .canonicalizers.base import ShockCanonicalizer
from macro_nowcast.storage.datasets import DATASETS


@dataclass(frozen=True)
class ShockSourceSpec:
    name: str
    domain: Literal["shocks"] = "shocks"
    canonicalizer: type[ShockCanonicalizer]
    canonical_key: str


SHOCK_SOURCES: dict[str, ShockSourceSpec] = {
    "tiingo": ShockSourceSpec(
        name="tiingo",
        canonicalizer=TiingoShockCanonicalizer,
        canonical_key=DATASETS.canonical.shocks_tiingo,
    ),
}