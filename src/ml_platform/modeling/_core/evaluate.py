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

    def improvement_over(self, *, other: Metric) -> float:
        if self.name != other.name:
            raise ValueError("Cannot compare metrics with different names.")
        
        if self.higher_is_better != other.higher_is_better:
            raise ValueError("Cannot compare metrics with different optimization directions.")
        
        if self.value == other.value:
            return 0.0
        
        if abs(other.value) < 1e-12:
            raise ValueError("Cannot compute relative improvement over zero.")

        if self.higher_is_better:
            return (self.value - other.value) / abs(other.value)
        else:
            return (other.value - self.value) / abs(other.value)


class Metrics(Protocol):
    def to_dict(self) -> dict[str, float]: ...
    def get_metric(self, *, name: str) -> Metric: ...
        

MetricsT = TypeVar("MetricsT", bound=Metrics)


class Scorer(ABC, Generic[MetricsT]):
    @abstractmethod
    def score(self, *, predictions: Predictions) -> MetricsT:
        raise NotImplementedError