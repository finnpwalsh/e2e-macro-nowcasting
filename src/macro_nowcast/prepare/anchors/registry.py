from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from macro_nowcast.interfaces import SourceDefinition
from .canonicalizers import AnchorCanonicalizer, FREDAnchorCanonicalizer
from macro_nowcast.storage import DATASETS


@dataclass(frozen=True)
class AnchorSourceDefinition(SourceDefinition):
    canonicalizer: Type[AnchorCanonicalizer]
    domain: str = "anchors"


ANCHOR_SOURCES: dict[str, AnchorSourceDefinition] = {
    "fred": AnchorSourceDefinition(
        name="fred",
        canonicalizer=FREDAnchorCanonicalizer,
        canonical_key=DATASETS.canonical.anchors_fred
    ),
}