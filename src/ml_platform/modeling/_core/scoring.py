from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .metrics import Metrics
from .predictions import Predictions


MetricsT = TypeVar("MetricsT", bound=Metrics)


class Scorer(ABC, Generic[MetricsT]):
    @abstractmethod
    def score(self, *, predictions: Predictions) -> MetricsT:
        raise NotImplementedError