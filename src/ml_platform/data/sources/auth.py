from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


AuthType = Literal["none", "api_key"]


@dataclass(frozen=True)
class AuthConfig:
    type: AuthType
    key_name: str | None = None