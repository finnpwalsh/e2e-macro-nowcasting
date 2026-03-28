from __future__ import annotations

from typing import Protocol


class Metric(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def value(self) -> str: ...


class Metrics(Protocol):
    def to_dict(self) -> dict[str, float]: ...