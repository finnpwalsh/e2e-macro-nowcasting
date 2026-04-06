from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from ml_platform.datasets import ResidualsService

from .cli import resolve_residuals_config
from .config import ResidualsConfig


def run(storage: Storage, config: ResidualsConfig) -> None:
    ResidualsService().run(
        storage=storage,
        run_family=config.run_family,
        target=config.target,
    )


def main() -> None:
    load_dotenv()
    run(
        storage=get_storage(),
        config=resolve_residuals_config(),
    )

if __name__ == "__main__":
    main()