from __future__ import annotations

from typing import Protocol


class Metrics(Protocol):
    def to_dict(self) -> dict[str, float]: ...

    def get_value(self, name: str) -> float:
        values = self.to_dict()
        try: 
            return values[name]
        except KeyError as e:
            available = ", ".join(sorted(values))
            raise ValueError(
                f"Unknown metric '{name}'. Available metrics: {available}"
            ) from e