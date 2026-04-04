from __future__ import annotations

from ml_platform.storage import Storage
from ml_platform.storage.serde import read_json
from ml_platform.storage.keys import PointerKeys
from ml_platform.runs.schema import RunPointer, RunSummary, ResolvedRun

from .schema import ResolvedTargets, PromotionMetrics


class PromotionResolver:
    def resolve_targets(
        storage: Storage,
        model_name: str,
    ) -> ResolvedTargets:

        pointers = PointerKeys(model_name=model_name)
        
        # -----------------------------------------------
        # Challenger
        # -----------------------------------------------

        challenger_pointer = RunPointer(**read_json(
            storage=storage,
            key=pointers.latest,
        ))

        challenger_summary = RunSummary(**read_json(
            storage=storage,
            key=challenger_pointer.summary_key,
        ))

        challenger = ResolvedRun(
            pointer=challenger_pointer,
            summary=challenger_summary,
        )

        # -----------------------------------------------
        # Champion
        # -----------------------------------------------

        try:
            champion_pointer = RunPointer(**read_json(
                storage=storage,
                key=pointers.champion,
            ))
        except FileNotFoundError:
            return ResolvedTargets(
                challenger=challenger,
                champion=None,
            )
        
        champion_summary = RunSummary(**read_json(
            storage=storage,
            key=champion_pointer.summary_key,
        ))

        champion = ResolvedRun(
            pointer=champion_pointer,
            summary=champion_summary,
        )

        # -----------------------------------------------
        # Resolve inputs
        # -----------------------------------------------

        return ResolvedTargets(
            challenger=challenger,
            champion=champion,
        )
    
    def resolve_metrics(
            targets: ResolvedTargets,
            promotion_metric_name: str,
    ) -> PromotionMetrics:
        champion = targets.champion
        challenger = targets.challenger
        
        if champion is None:
            champion_metric = None
        else:
            champion_metric = champion.summary.metrics.get_metric(promotion_metric_name)
        
        challenger_metric = challenger.summary.metrics.get_metric(promotion_metric_name)
        
        return PromotionMetrics(
            challenger_metric=challenger_metric,
            champion_metric=champion_metric,
        )