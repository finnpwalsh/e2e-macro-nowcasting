from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable, TypeVar


T = TypeVar("T")


def resolve_config(parse_fn: Callable[[Any], T]) -> T:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    path = Path(args.config)

    if not path.exists():
        raise SystemExit(f"--config file does not exist: {path}")
    
    if not path.is_file():
        raise SystemExit(f"--config must point to a file: {path}")
    
    try:
        raw = path.read_text(encoding="utf-8")
        value = json.loads(raw)
    except Exception as e:
        raise SystemExit(f"Failed to load config '{path}': {e}") from e

    return parse_fn(value)