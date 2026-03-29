from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrainingRunConfig:
    run_family: str
    input_key: str