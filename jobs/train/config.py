from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class TrainingRunConfig:
    run_family: str
    input_key: str
    target_col: str
    row_id_col: str | None = None
    extras: Mapping[str, str] | None = None