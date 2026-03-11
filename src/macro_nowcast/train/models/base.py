from __future__ import annotations

from typing import Protocol
from sklearn.pipeline import Pipeline


class ModelSpec(Protocol):
    """
    Lightweight base class for trainable models.
    """

    def make_pipeline(self) -> Pipeline:
        """
        Return a fully configured sklearn Pipeline.
        """
        ...