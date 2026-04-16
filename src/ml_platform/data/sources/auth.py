from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


AuthType = Literal["none", "api_key"]


@dataclass(frozen=True)
class AuthConfig:
    type: AuthType
    key_name: str | None = None

    def validate(self) -> None:
        if self.type == "none":
            if self.key_name is not None:
                raise ValueError(
                    "AuthConfig: key_name must be None when type='none'."
                )
        
        if self.type == "api_key":
            if not self.key_name:
                raise ValueError(
                    "AuthConfig: key_name is required when type = 'api_key'."
                )
        
        else:
            raise ValueError(
                f"AuthConfig: unsupported auth type: '{self.type}'."
            )