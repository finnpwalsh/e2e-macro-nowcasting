"""
Select job: promote a specified registered model version to an alias (champion).

Lifecycle stage:
    Select

Responsibilities:
    - Promote a specified registered model version to a named alias
    - Mutate a single control-plane pointer (registry alias)

Inputs:
    - Registry model name (MLFLOW_REGISTRY_MODEL_NAME or default)
    - Target alias name (MLFLOW_MODEL_ALIAS or default)
    - Target model version to promote (MLFLOW_PROMOTE VERSION)

Outputs:
    - Updated registry alias pointer (e.g. champion -> specified version)

Out of scope:
    - Model training or retraining
    - Publishing metrics or artifacts (tracking)
    - Model comparison or selection logic
    - Online serving or inference

Notes:
    Selection is control-plane only. This job mutates exactly one registry alias
    and does not touch training artifacts or datasets.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

from ml_platform.mlflow.promote import promote_latest


def promote() -> None:
    registry_name = "baseline"
    alias = "champion"
    version = os.getenv("MLFLOW_PROMOTE_VERSION").strip()

    if not version:
        raise RuntimeError(
            "Missing required env var: MLFLOW_PROMOTE_VERSION "
            "(explicit model registry version to promote)"
        )

    written = promote_latest(
        registry_name,
        alias=alias,
        version=version,
    )

    INDENT = "    "
    print()
    print("MLflow promotion complete")
    print(f"{INDENT}Registry Name:  {written['registry_model_name']}")
    print(f"{INDENT}Alias:          {written['alias']}")
    print(f"{INDENT}Version:        {written['version']}")
    print(f"{INDENT}Model URI:      {written['model_uri']}")


def main() -> None:
    load_dotenv()
    promote()


if __name__ == "__main__":
    main()