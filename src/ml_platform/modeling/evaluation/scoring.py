from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..core.predictions import Predictions
from ..core.metrics import Metrics


MetricsT = TypeVar("MetricsT", bound=Metrics)


class Scorer(ABC, Generic[MetricsT]):
    @abstractmethod
    def score(self, *, predictions: Predictions) -> MetricsT:
        raise NotImplementedError