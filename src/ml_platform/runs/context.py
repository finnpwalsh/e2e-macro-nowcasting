from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from ml_platform.storage.keys import Keys
from .schema import RunIdentity


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def create_run_identity(*, run_family: str) -> "RunIdentity":
    created_at_utc = utc_now()
    run_id = f"{created_at_utc}_{uuid4().hex[:12]}"
    return RunIdentity(
        run_family=run_family,
        run_id=run_id,
        created_at_utc=created_at_utc,
    )
        

# -----------------------------
# Run context
# -----------------------------

@dataclass(frozen=True)
class RunContext:
    identity: RunIdentity
    
    @property
    def run_family(self) -> str:
        return self.identity.run_family
    
    @property
    def run_id(self) -> str:
        return self.identity.run_id
    
    @property
    def created_at_utc(self) -> str:
        return self.identity.created_at_utc
    
    @property
    def keys(self) -> Keys:
        return Keys(self.run_family, self.run_id)
    
    @classmethod
    def create(cls, *, run_family: str) -> "RunContext":
        return cls(identity=create_run_identity(run_family=run_family))