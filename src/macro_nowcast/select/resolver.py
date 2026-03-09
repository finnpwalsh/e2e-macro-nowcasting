from __future__ import annotations

from ml_platform.storage import Storage, read_json
from ml_platform.storage.keys import PointerKeys
from ml_platform.runs.manifests import Pointer, RunSummary

from .schema import ResolvedRun, ResolvedSelectionInputs


class SelectionResolver:
    def resolve(
        self,
        *,
        storage: Storage,
        model_name: str,
    ) -> ResolvedSelectionInputs:
        
        # -----------------------------------------------
        # Pointers
        # -----------------------------------------------

        pointers = PointerKeys(model_name="baseline")
        
        # -----------------------------------------------
        # Challenger
        # -----------------------------------------------

        challenger_pointer: Pointer = read_json(
            storage=storage,
            key=pointers.latest,
        )

        challenger_summary: RunSummary = read_json(
            storage=storage,
            key=challenger_pointer.summary_key,
        )

        challenger = ResolvedRun(
            pointer=challenger_pointer,
            summary=challenger_summary,
        )

        # -----------------------------------------------
        # Champion
        # -----------------------------------------------

        try:
            champion_pointer: Pointer = read_json(
                storage=storage,
                key=pointers.champion,
            )
        except FileNotFoundError:
            return ResolvedSelectionInputs(
                challenger=challenger,
                champion=None,
            )
        
        champion_summary: RunSummary = read_json(
            storage=storage,
            key=champion_pointer.summary_key,
        )

        champion = ResolvedRun(
            pointer=champion_pointer,
            summary=champion_summary,
        )

        # -----------------------------------------------
        # Resolve inputs
        # -----------------------------------------------

        return ResolvedSelectionInputs(
            challenger=challenger,
            champion=champion,
        )