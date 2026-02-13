"""
Artifact contract layer.

Defines:
    - Immutable run-scoped artifact keys (TrainArtifacts, EvalArtifacts)
    - Mutable lifecycle pointers (ModelPointers)
"""
from .keys import TrainArtifacts, EvalArtifacts
from .pointers import ModelPointers
from .ids import new_run_id

__all__ = [
    "TrainArtifacts",
    "EvalArtifacts",
    "ModelPointers",
    "new_run_id",
]