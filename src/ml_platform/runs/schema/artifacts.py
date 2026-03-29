from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class RunArtifacts:
    primary: str | None = None
    extras: Mapping[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, str]:
        out: dict[str, str] = {}

        if self.primary is not None:
            out["primary"] = self.primary
        
        out.update(dict(self.extras))
        return out