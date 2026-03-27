from __future__ import annotations

from typing import Protocol, TypeVar
from ml_platform.artifacts.predictions import Predictions


MetricsT = TypeVar("MetricsT", bound=Metrics)
InputT = TypeVar("InputT")


class Metrics(Protocol):
    def to_dict(self) -> dict[str, float]: ...


class Scorer(Protocol[InputT, MetricsT]):
    def score(self, *, evaluation_input: InputT) -> MetricsT: ...


class Evaluator(Protocol[MetricsT]):
    def evaluate(
            self,
            *,
            predictions: Predictions,
    ) -> MetricsT: ...