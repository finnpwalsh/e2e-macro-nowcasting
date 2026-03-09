from __future__ import annotations

from dataclasses import dataclass

from ml_platform.runs.manifests import Pointer
from ml_platform.runs.write_plan import JsonWrite, WritePlan
from ml_platform.storage import Storage
from ml_platform.storage.keys import PointerKeys

from .decider import ChampionDecider
from .resolver import SelectionResolver
from .schema import ResolvedSelectionInputs, SelectorResult


@dataclass(frozen=True)
class ChampionSelector:
    model_name: str

    def select(self, *, storage: Storage) -> SelectorResult:
        resolved: ResolvedSelectionInputs = SelectionResolver(
            storage=storage,
            model_name=self.model_name,
        )

        challenger = resolved.challenger
        champion = resolved.champion

        decision = ChampionDecider().decide(
            challenger_metrics=challenger.summary.primary_metric,
            champion_metrics=None if champion is None else champion.summary.primary_metric,
        )

        if decision.selected == "challenger":
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

        return SelectorResult(
            challenger=challenger.pointer,
            champion_before=None if champion is None else champion.pointer,
            champion_after=champion_after,
            decision=decision,
            write_plan=WritePlan(writes=writes)
        )