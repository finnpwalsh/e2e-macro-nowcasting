from __future__ import annotations

from dataclasses import dataclass

from ml_platform.runs.schema import RunPointer, RunSummary
from ml_platform.storage.persistence import PersistencePlan


@dataclass(frozen=True)
class ResolvedRun:
    pointer: RunPointer
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
    challenger: RunPointer
    champion_before: RunPointer | None
    champion_after: RunPointer
    decision: SelectionDecision
    persistence_plan: PersistencePlan