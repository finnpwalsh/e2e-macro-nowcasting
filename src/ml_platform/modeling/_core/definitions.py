from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any

import json


@dataclass(frozen=True)
class ModelDefinition:
    engine: str
    name: str
    params: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine": self.name,
            "name": self.name,
            "params": dict(self.params),
        }


def parse_model_definition(raw: str) -> ModelDefinition:
    try:
        value: Any = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"--model-def must be valid JSON: {e}") from e

    if not isinstance(value, dict):
        raise SystemExit("--model-def must deserialize to a JSON object.")

    engine = value.get("engine")
    if not isinstance(engine, str) or not engine.strip():
        raise SystemExit("--model-def['engine'] must be a non-empty string.")

    model = value.get("model")
    if not isinstance(model, str) or not model.strip():
        raise SystemExit("--model-def['model'] must be a non-empty string.")

    params = value.get("params", {})
    if not isinstance(params, dict):
        raise SystemExit("--model-def['params'] must be an object.")

    return ModelDefinition(
        engine=engine.strip(),
        name=model.strip(),
        params=params,
    )