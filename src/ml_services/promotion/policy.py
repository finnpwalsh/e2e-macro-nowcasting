from __future__ import annotations

from .schema import PromotionDecision, PromotionMetrics, PromotionTarget


class PromotionPolicy:
    def decide(
        self,
        *,
        promotion_metrics: PromotionMetrics,
        minimum_proportional_improvement: float
    ) -> PromotionDecision:
        if promotion_metrics.champion_metric is None:
            return PromotionDecision(
                chosen=PromotionTarget.CHALLENGER,
                challenger_metric=promotion_metrics.challenger_metric,
                champion_metric=None,
            )
        
        improvement = (
            promotion_metrics.challenger_metric
            .improvement_over(other=promotion_metrics.champion_metric)
        )
        
        if (improvement > minimum_proportional_improvement):
            chosen = PromotionTarget.CHALLENGER
        else:
            chosen = PromotionTarget.CHAMPION
        
        return PromotionDecision(
            chosen=chosen,
            challenger_metric=promotion_metrics.challenger_metric,
            champion_metric=promotion_metrics.champion_metric,
        )