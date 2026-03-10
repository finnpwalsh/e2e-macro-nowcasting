from __future__ import annotations

from typing import Mapping

from .schema import SelectionDecision


class ChampionDecider:
    def decide(
        self,
        *,
        challenger_metrics: Mapping[str, float],
        champion_metrics: Mapping[str, float] | None,
    ) -> SelectionDecision:
        
        challenger_rmse = float(challenger_metrics["rmse"])
        
        # -----------------------------------------------
        # No current champion
        # -----------------------------------------------

        if champion_metrics is None:
            return SelectionDecision(
                selected="challenger",
                challenger_rmse=challenger_rmse,
                champion_rmse=None,
            )
        
        champion_rmse = float(champion_metrics["rmse"])

        # -----------------------------------------------
        # Decide
        # -----------------------------------------------

        if challenger_rmse < champion_rmse:
            return SelectionDecision(
                selected="challenger",
                challenger_rmse=challenger_rmse,
                champion_rmse=champion_rmse,
            )