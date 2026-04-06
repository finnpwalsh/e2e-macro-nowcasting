from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ResidualsConfig:
    run_family: str
    target: Literal["latest", "champion"]