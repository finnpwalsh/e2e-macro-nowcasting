from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from ml_platform.storage.serde import write_json
from ml_platform.runs.write_plan import JsonWrite
from macro_nowcast.select.selector import ChampionSelector


def run(storage: Storage) -> None:
    selector = ChampionSelector(model_name="baseline")
    result = selector.select(storage=storage)

    for write in result.write_plan.writes:
        if isinstance(write, JsonWrite):
            write_json(
                storage=storage,
                key=write.key,
                payload=write.payload,
            )
    
    champion = result.champion_after
    decision = result.decision
    rmse = decision.challenger_rmse if decision.selected == "challenger" else decision.champion_rmse

    INDENT = "    "
    SUB = INDENT * 2
    print(f"\n[SELECT][RUN] Complete")
    print(f"{INDENT}Model name: {champion.model_name}")
    print(f"{INDENT}Selected:   {decision.selected}")
    print(f"{INDENT}[CHAMPION]")
    print(f"{SUB}Run ID:             {champion.run_id}")
    print(f"{SUB}Summary key:        {champion.summary_key}")
    print(f"{SUB}Manifest key:       {champion.manifest_key}")
    print(f"{SUB}Model artifact key: {champion.model_artifact_key}")
    print(f"{SUB}RMSE:               {rmse}")


def main() -> None:
    load_dotenv()
    run(get_storage())


if __name__ == "__main__":
    main()