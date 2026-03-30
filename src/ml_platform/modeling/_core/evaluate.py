from __future__ import annotations

from typing import TypeVar, Protocol, Generic
from abc import ABC, abstractmethod

from .predictions import Predictions


class Metrics(Protocol):
    def to_dict(self) -> dict[str, float]: ...

    def get_value(self, name: str) -> float:
        values = self.to_dict()
        try: 
            return values[name]
        except KeyError as e:
            available = ", ".join(sorted(values))
            raise ValueError(
                f"Unknown metric '{name}'. Available metrics: {available}"
            ) from e
        

MetricsT = TypeVar("MetricsT", bound=Metrics)


class Scorer(ABC, Generic[MetricsT]):
    @abstractmethod
    def score(self, *, predictions: Predictions) -> MetricsT:
        raise NotImplementedError