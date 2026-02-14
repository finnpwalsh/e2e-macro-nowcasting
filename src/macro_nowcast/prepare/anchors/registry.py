from __future__ import annotations

from typing import Type

from .canonicalizers.fred import FREDAnchorCanonicalizer

ANCHOR_CANONICALIZERS: dict[str, Type] = {
    "fred": FREDAnchorCanonicalizer,
}