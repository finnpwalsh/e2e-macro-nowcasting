from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

from ..storage import Storage

from .writes import WriteOp


@dataclass(frozen=True)
class PersistencePlan:
    writes: Sequence[WriteOp]

    def persist(self, *, storage: Storage) -> None:
        for write in self.writes:
            write.persist(storage=storage)
    
    def extend(self, more_writes: Sequence[WriteOp]) -> "PersistencePlan":
        return PersistencePlan(writes=[*self.writes, *more_writes])