from __future__ import annotations

from typing import Generic, TypeVar, Protocol
from abc import ABC, abstractmethod


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
        

EvaluationInputT = TypeVar("EvaluationInputT")
EvaluationResultT = TypeVar("EvaluationResultT")
MetricsT = TypeVar("MetricsT", bound=Metrics)


class Scorer(ABC, Generic[EvaluationInputT, MetricsT]):
    @abstractmethod
    def score(self, *, evaluation_input: EvaluationInputT) -> MetricsT:
        raise NotImplementedError


class EvaluationWorkflow(Protocol, Generic[EvaluationInputT, EvaluationResultT]):
    scorer: Scorer

    def evaluate(
        self,
        *,
        evaluation_input: EvaluationInputT,
    ) -> EvaluationResultT: ...