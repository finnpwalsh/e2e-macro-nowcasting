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
    test.txt
```

3. Build 4 images (ETL/Train/Track/Serve)
4. Swap DAG tasks to container execution (DockerOperator locally then ECSOperator next)


## repo refactor

1. update modular calls with refactored `src` directory naming, e.g. `src.config.baseline` -> `src.train.baseline.contracts`
2. refactor `tests/`

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
