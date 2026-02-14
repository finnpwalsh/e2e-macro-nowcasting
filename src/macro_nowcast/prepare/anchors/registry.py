from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from .canonicalizers.fred import FREDAnchorCanonicalizer
from macro_nowcast.interfaces.canonicalizer import Canonicalizer

from macro_nowcast.storage.datasets import DATASETS


@dataclass(frozen=True)
class AnchorSourceSpec:
    name: str
    canonicalizer: Type[Canonicalizer]
    canonical_key: str


ANCHOR_SOURCES: dict[str, AnchorSourceSpec] = {
    "fred": AnchorSourceSpec(
        name="fred",
        canonicalizer=FREDAnchorCanonicalizer,
        canonical_key=DATASETS.canonical.anchors_fred
    ),
}