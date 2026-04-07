from __future__ import annotations

from dataclasses import dataclass

from .keys import RunKeys
from .identity import RunIdentity


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
    def keys(self) -> str:
        return RunKeys(run_family=self.run_family, run_id=self.run_id)