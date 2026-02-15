from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .canonicalizers import AnchorCanonicalizer, FREDAnchorCanonicalizer
from macro_nowcast.storage import DATASETS


@dataclass(frozen=True)
class AnchorSourceSpec:
    name: str
    domain: Literal["anchors"] = "anchors"
    canonicalizer: type[AnchorCanonicalizer]
    canonical_key: str


ANCHOR_SOURCES: dict[str, AnchorSourceSpec] = {
    "fred": AnchorSourceSpec(
        name="fred",
        canonicalizer=FREDAnchorCanonicalizer,
        canonical_key=DATASETS.canonical.anchors_fred
    ),
}