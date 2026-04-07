from __future__ import annotations

from typing import Protocol

from .metric import Metric


class Metrics(Protocol):
    def to_dict(self) -> dict[str, float]: ...
    def get_metric(self, *, metric: str) -> Metric: ...