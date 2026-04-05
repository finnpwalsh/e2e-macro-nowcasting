from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ml_platform.modeling._core import ModelDefinition


@dataclass(frozen=True)
class RunConfig:
    run_family: str
    input_key: str
    target_col: str
    row_id_col: str | None = None


@dataclass(frozen=True)
class SplitConfig:
    type: Literal["time"]

    # time
    time_col: str
    split_date: str


@dataclass(frozen=True)
class TrainingConfig:
    run: RunConfig
    split: SplitConfig
    model: ModelDefinition