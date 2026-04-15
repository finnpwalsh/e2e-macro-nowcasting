from __future__ import annotations

from typing import Protocol, Mapping, Any

from .protocols import FitPredictModel


class ModelSpec(Protocol):
    def build(
        self,
        *,
        params: Mapping[str, Any] | None = None,
    ) -> FitPredictModel: ...