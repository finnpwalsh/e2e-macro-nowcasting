from __future__ import annotations

import os

from .base import SecretResolver


class EnvSecretResolver(SecretResolver):
    """
    Resolves secrets from environmental variables.

    Ideal for:
         - local dev
         - Docker containers
         - ECS task definitions
    """

    def get(self, name: str) -> str:
        value = os.getenv(name)
        if value is None:
            raise ValueError(
                f"Missing required environmental variable: '{name}'. "
                "Ensure it is set in your runtime environment."
            )
        
        return value