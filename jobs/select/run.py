from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from ml_platform.promotion import PromotionService

from .cli import resolve_selection_config
from .config import SelectionConfig


def run(storage: Storage, config: SelectionConfig) -> None:

    # -----------------------------------------------------
    # Select champion
    # -----------------------------------------------------

    service = PromotionService(run_family=config.target.run_family)
    result = service.run(
        storage=storage,
        primary_metric=config.policy.primary_metric,
        minimum_proportional_improvement=config.policy.minimum_proportional_improvement,
    )

    # -----------------------------------------------------
    # Persist
    # -----------------------------------------------------

    result.persistence_plan.persist(storage=storage)


def main() -> None:
    load_dotenv()
    config = resolve_selection_config()
    run(get_storage(), config=config)


if __name__ == "__main__":
    main()