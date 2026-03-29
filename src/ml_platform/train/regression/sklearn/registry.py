from __future__ import annotations

from .specs import SklearnModelSpec, RidgeSpec


class SklearnSpecRegistry:
    specs: dict[str, SklearnModelSpec]

    def get(self, name: str) -> SklearnModelSpec:
        try:
            return self.specs[name]
        except KeyError as e:
            available = ", ".join(sorted(self.specs))
            raise ValueError(
                f"Unknown model spec '{name}. Available specs: {available}"
            ) from e


SKLEARN_SPECS = SklearnSpecRegistry(
    specs={
        "ridge": RidgeSpec(),
    }
)