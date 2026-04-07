from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .identity import RunIdentity


@dataclass(frozen=True)
class RunPointer:
    run_identity: RunIdentity
    updated_at_utc: str

    @classmethod
    def create(cls, *, run_identity: RunIdentity) -> "RunPointer":
        return cls(
            run_identity=run_identity,
            updated_at_utc=datetime.now(timezone.utc).isoformat(),
        )