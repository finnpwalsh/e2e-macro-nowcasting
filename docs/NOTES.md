## repo refactor

1. add README.md for `src/` + update README for `scripts/`
2. refactor `tests/`

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

3. update modular `test/` calls with refactored `src/` directory naming, e.g. `src.config.baseline` -> `src.train.baseline.contracts`
4. add lightweight README for `tests/`
5. (maybe) add README for `src/` subfolders

---


## containerized orchestraction refactor

1. Refactor requirement files
```
requirements/
    base.txt
    etl.txt
    train.txt
    track.txt
    serve.txt
    dev.txt
```

2. Docker refactor

```
infra/docker/
  base/
    Dockerfile

  etl/
    Dockerfile

  train/
    Dockerfile

  track/
    Dockerfile

  serve/
    Dockerfile
```

3. Build images (ETL/Train/Track/Serve)
4. Swap DAG tasks to container execution (DockerOperator locally then ECSOperator next)