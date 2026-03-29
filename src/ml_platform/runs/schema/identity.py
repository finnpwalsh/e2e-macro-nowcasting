from __future__ import annotations

from dataclasses import dataclass


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