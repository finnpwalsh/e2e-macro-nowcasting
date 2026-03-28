from __future__ import annotations

from typing import Protocol, TypeVar

from .schema import Metrics


InputT = TypeVar("InputT")
MetricsT = TypeVar("MetricsT", bound=Metrics)


class Scorer(Protocol[InputT, MetricsT]):
    def score(self, *, evaluation_input: InputT) -> MetricsT: ...


class Evaluator(Protocol[InputT, MetricsT]):
    def evaluate(self, *, evaluation_input: InputT) -> MetricsT: ...