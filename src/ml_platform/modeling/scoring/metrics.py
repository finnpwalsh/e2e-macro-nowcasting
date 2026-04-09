from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Metric:
    metric: str
    value: float
    higher_is_better: bool

    def to_dict(self) -> dict:
        return {
            "metric": self.metric,
            "value": self.value,
            "higher_is_better": self.higher_is_better,
        }


class Metrics(Protocol):
    def to_dict(self) -> dict[str, float]: ...
    def get_metric(self, *, metric: str) -> Metric: ...