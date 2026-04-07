from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class RunIdentity:
    run_family: str
    run_id: str
    created_at_utc: str

    def to_dict(self) -> dict[str, str]:
        return {
            "run_family": self.run_family,
            "run_id": self.run_id,
            "created_at_utc": self.created_at_utc,
        }
    
    @classmethod
    def create(cls, *, run_family: str) -> "RunIdentity":
        created_at_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_id = f"{created_at_utc}_{uuid4().hex[:12]}"
        
        return cls(
            run_family=run_family,
            run_id=run_id,
            created_at_utc=created_at_utc,
        )