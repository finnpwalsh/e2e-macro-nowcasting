from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Protocol, Generic
from abc import ABC, abstractmethod

from .predictions import Predictions


@dataclass(frozen=True)
class Metric:
    name: str
    value: float
    higher_is_better: bool

    def compare_to(self, *, other: Metric) -> int:
        if self.name != other.name:
            raise ValueError("Cannot compare metrics with different names.")
        if self.value == other.value: return 0

        if self.higher_is_better:
            return 1 if self.value > other.value else -1
        else:
            return -1 if self.value > other.value else 1


class Metrics(Protocol):
    def to_dict(self) -> dict[str, float]: ...
    def get_metric(self, *, name: str) -> Metric: ...
        

MetricsT = TypeVar("MetricsT", bound=Metrics)


class Scorer(ABC, Generic[MetricsT]):
    @abstractmethod
    def score(self, *, predictions: Predictions) -> MetricsT:
        raise NotImplementedError