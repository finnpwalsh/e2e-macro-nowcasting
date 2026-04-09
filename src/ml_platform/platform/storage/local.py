"""Local filesystem implementation of Storage."""
from __future__ import annotations

from pathlib import Path


class LocalStorage:
    def read_bytes(self, key: str) -> bytes:
        path = Path(key)

        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")
        
        return path.read_bytes()
    
    def write_bytes(self, key: str, data: bytes) -> None:
        path = Path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def exists(self, key: str) -> bool:
        return Path(key).exists()
    
    def list(self, prefix: str) -> list[str]:
        path = Path(prefix)

        if path.is_file():
            return [str(path)]
        
        if not path.exists():
            return []
        
        return [
            str(p)
            for p in path.rglob("*")
            if p.is_file()
        ]