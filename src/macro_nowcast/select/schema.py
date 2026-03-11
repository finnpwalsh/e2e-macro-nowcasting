from __future__ import annotations

from dataclasses import dataclass

from ml_platform.runs.manifests import Pointer, RunSummary
from ml_platform.runs.persistence import PersistencePlan


@dataclass(frozen=True)
class ResolvedRun:
    pointer: Pointer
    summary: RunSummary


@dataclass(frozen=True)
class ResolvedSelectionInputs:
    challenger: ResolvedRun
    champion: ResolvedRun | None


@dataclass(frozen=True)
class SelectionDecision:
    selected: str
    challenger_rmse: dict[str, float]
    champion_rmse: dict[str, float]


@dataclass(frozen=True)
class SelectorResult:
    challenger: Pointer
    champion_before: Pointer | None
    champion_after: Pointer
    decision: SelectionDecision
    persistence_plan: PersistencePlan