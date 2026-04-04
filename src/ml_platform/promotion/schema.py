from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ml_platform.runs.schema import RunPointer, ResolvedRun
from ml_platform.storage.persistence import PersistencePlan
from ml_platform.modeling._core import Metric


@dataclass(frozen=True)
class ResolvedTargets:
    challenger: ResolvedRun
    champion: ResolvedRun | None


class PromotionTarget(str, Enum):
    CHALLENGER = "challenger"
    CHAMPION = "champion"


@dataclass(frozen=True)
class PromotionDecision:
    chosen: PromotionTarget
    challenger_metrics: dict[str, float]
    champion_metrics: dict[str, float] | None


@dataclass(frozen=True)
class PromotionResult:
    challenger: RunPointer
    champion_before: RunPointer | None
    champion_after: RunPointer
    decision: PromotionDecision
    persistence_plan: PersistencePlan


@dataclass(frozen=True)
class PromotionMetrics:
    challenger_metric: Metric
    champion_metric: Metric | None