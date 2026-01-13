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

1. Add infra/docker/runtimes and services READMEs (copy/paste from infra/Docker README) OR restructure infra/docker README by runtimes vs. services
2. Update Docker requirements installs with new directories (e.g. requirements/runtimes/etl.txt)
3. Build images (ETL/Train/Track/Serve)
4. Swap DAG tasks to container execution (DockerOperator locally then ECSOperator next)