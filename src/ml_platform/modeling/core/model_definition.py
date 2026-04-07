from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Task(str, Enum):
    REGRESSION = "regression"
    CLASSIFICATION = "classification"


@dataclass(frozen=True)
class ModelDefinition:
    engine: str
    task: Task
    name: str
    params: dict

    def to_dict(self) -> dict:
        return {
            "engine": self.engine,
            "task": self.task,
            "name": self.name,
            "params": self.params,
        }