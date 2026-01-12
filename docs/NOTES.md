## tests refactor

1. refactor `tests/`

```
tests/
    etl/
        anchors/
            fred/
        shocks/
            yfinance/
        assemble/
    
    train/
        baseline/
    
    track/
        mlflow/
    
    common/
        evaluation/
        storage/
```

2. update modular `test/` calls with refactored `src/` directory naming, e.g. `src.config.baseline` -> `src.train.baseline.contracts`
3. add lightweight README for `tests/`

---


## containerized orchestraction refactor

1. Add infra/docker README
2. restructure requirements

```
requirements/
    base.txt
    runtimes/
```

3. Build images (ETL/Train/Track/Serve)
4. Swap DAG tasks to container execution (DockerOperator locally then ECSOperator next)