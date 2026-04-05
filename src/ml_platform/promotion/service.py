from __future__ import annotations

from dataclasses import dataclass

from ml_platform.storage import (
    Storage,
    PersistencePlan,
    JsonWrite,
)
from ml_platform.storage.keys import PointerKeys

from .policy import PromotionPolicy
from .resolver import PromotionResolver
from .schema import ResolvedTargets, PromotionResult, PromotionTarget, PromotionMetrics


@dataclass(frozen=True)
class PromotionService:
    model_family: str

    def run(
        self,
        *,
        storage: Storage,
        primary_metric: str,
        minimum_proportional_improvement: float,
    ) -> PromotionResult:
        targets: ResolvedTargets = PromotionResolver().resolve_targets(
            storage=storage,
            model_family=self.model_family,
        )

        challenger = targets.challenger
        champion = targets.champion

        promotion_metrics: PromotionMetrics = PromotionResolver().resolve_metrics(
            targets=targets,
            primary_metric=primary_metric,
        )

        decision = PromotionPolicy().decide(
            promotion_metrics=promotion_metrics,
            minimum_proportional_improvement=minimum_proportional_improvement,
        )

        if decision.chosen == PromotionTarget.CHALLENGER:
            champion_after = challenger.pointer
            writes = [
                JsonWrite(
                    key=PointerKeys(model_name=self.model_name).champion,
                    payload=champion_after,
                )
            ]
        else:
            champion_after = champion.pointer
            writes = []

        return PromotionResult(
            challenger=challenger.pointer,
            champion_before=None if champion is None else champion.pointer,
            champion_after=champion_after,
            decision=decision,
            persistence_plan=PersistencePlan(writes=writes)
        )