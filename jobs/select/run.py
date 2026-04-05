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

    service = PromotionService(model_name=config.target.model_family)
    result = service.run(
        storage=storage,
        promotion_metric_name=config.policy.primary_metric,
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