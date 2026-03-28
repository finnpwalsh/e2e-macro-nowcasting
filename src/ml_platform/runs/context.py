from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from ml_platform.storage.keys import Keys


# -----------------------------
# Run id
# -----------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

class RunId:
    def __init__(self):
        self.created_at_utc = utc_now()
        self._nonce = uuid4().hex[:12]
        self.value = f"{self.created_at_utc}_{self._nonce}"
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"RunId({self.value})"
        

# -----------------------------
# Run context
# -----------------------------

class RunContext:
    def __init__(self, run_family: str):
        self.run_family = run_family
        self._run_id = RunId()
    
    @property
    def run_id(self) -> str:
        return str(self._run_id)
    
    @property
    def created_at_utc(self) -> str:
        return self._run_id.created_at_utc
    
    @property
    def keys(self) -> Keys:
        return Keys(self.run_family, self.run_id)