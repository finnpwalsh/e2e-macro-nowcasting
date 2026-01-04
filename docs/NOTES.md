## repo refactor

1. refactor `src/etl/sources` into `src/etl/anchors` and `src/etl/shocks`
2. update modular `src/` calls with refactored `src/` directory naming, e.g. `src.config.baseline` -> `src.train.baseline.contracts`
3. add README.md for `src/`
4. refactor `tests/`

```
tests/
    etl/
        sources/
            fred/
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

5. update modular `test/` calls with refactored `src/` directory naming, e.g. `src.config.baseline` -> `src.train.baseline.contracts`
6. add lightweight README for `tests/`
7. (maybe) add README for `src/` subfolders

## containerized orchestraction refactor

1. Refactor training -> tracking split
- `train_ridge.py` writes artifacts + run.json
- `track_mlflow.py` logs + registers

2. Refactor requirement files
```
requirements/
    base.txt
    etl.txt
    train.txt
    track.txt
    serve.txt
    dev.txt
```

3. Docker refactor

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

4. Build images (ETL/Train/Track/Serve)
5. Swap DAG tasks to container execution (DockerOperator locally then ECSOperator next)