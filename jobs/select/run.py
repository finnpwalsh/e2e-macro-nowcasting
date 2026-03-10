from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from macro_nowcast.select.selector import ChampionSelector


def run(storage: Storage) -> None:

    # -----------------------------------------------------
    # Select champion
    # -----------------------------------------------------

    selector = ChampionSelector(model_name="baseline")
    result = selector.select(storage=storage)

    # -----------------------------------------------------
    # Persist
    # -----------------------------------------------------

    result.persistence_plan.persist(storage=storage)


def main() -> None:
    load_dotenv()
    run(get_storage())


if __name__ == "__main__":
    main()