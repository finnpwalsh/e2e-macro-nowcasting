from __future__ import annotations

from dataclasses import dataclass


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