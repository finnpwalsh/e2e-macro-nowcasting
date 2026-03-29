from __future__ import annotations

from typing import Generic, TypeVar
from abc import ABC, abstractmethod


EvaluationInputT = TypeVar("EvaluationInputT")
MetricsT = TypeVar("MetricsT")


class Scorer(ABC, Generic[EvaluationInputT, MetricsT]):
    @abstractmethod
    def score(self, *, evaluation_input: EvaluationInputT) -> MetricsT:
        raise NotImplementedError


class Evaluator(ABC, Generic[EvaluationInputT, MetricsT]):
    def evaluate(self, *, evaluation_input: EvaluationInputT) -> MetricsT:
        raise NotImplementedError