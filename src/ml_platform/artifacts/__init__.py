"""
Artifact contract layer.

Defines:
    - Immutable run-scoped artifact keys (TrainArtifacts, EvalArtifacts)
    - Mutable lifecycle pointers (ModelPointers)
"""
from .keys import TrainArtifacts, EvalArtifacts
from .pointers import ModelPointers

__all__ = [
    "TrainArtifacts",
    "EvalArtifacts",
    "ModelPointers",
]