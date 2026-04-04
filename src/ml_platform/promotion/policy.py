from __future__ import annotations

from .schema import PromotionDecision, PromotionMetrics, PromotionTarget


class PromotionPolicy:
    def decide(
        self,
        *,
        promotion_metrics: PromotionMetrics,
    ) -> PromotionDecision:
        if promotion_metrics.champion_metric is None:
            return PromotionDecision(
                chosen=PromotionTarget.CHALLENGER,
                challenger_metric=promotion_metrics.challenger_metric,
                champion_metric=None,
            )

        if promotion_metrics.challenger_metric.compare_to(promotion_metrics.champion_metric) > 0: 
            chosen = PromotionTarget.CHALLENGER
        else:
            chosen = PromotionTarget.CHAMPION
        
        return PromotionDecision(
            chosen=chosen,
            challenger_metric=promotion_metrics.challenger_metric,
            champion_metric=promotion_metrics.champion_metric,
        )