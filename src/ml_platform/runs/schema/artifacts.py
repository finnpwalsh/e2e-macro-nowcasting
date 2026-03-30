from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class RunArtifacts:
    primary: str | None = None
    extras: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if "primary" in self.extras:
            raise ValueError("'extras' may not contain reserved key 'primary'.")
        
    def to_dict(self) -> dict[str, str]:
        return {
            "primary": self.primary,
            "extras": dict(self.extras),
        }