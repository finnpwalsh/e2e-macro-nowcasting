from __future__ import annotations

import os
from pathlib import Path


def test_smoke_imports() -> None:
    import src
    import jobs
    import orchestration.airflow.dags.price_nowcasting

def test_smoke_local_storage(tmp_path: Path) -> None:

    from src.common.storage.backends.local import LocalStorage

    # save current working directory as-is, use a temporary
    # directory to test local storage I/O
    cwd = os.getcwd()
    try:
        os.chdir(tmp_path)

        storage = LocalStorage()

        payload = {"ok": True}
        outpath = "smoke/test.json"

        storage.write_json(outpath, payload)
        result = storage.read_json(outpath)

        assert result == payload
    finally:
        os.chdir(cwd)