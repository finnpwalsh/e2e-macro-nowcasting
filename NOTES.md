1. Refactor training -> tracking split
- `train_ridge.py` writes artifacts + run.json
- `track_mlflow.py` logs + registers

2. Define 3 requirement files
- `etl.txt`
- `train.txt`
- `track.txt`

3. Build 3 images (ETL/Train/Track)
4. Swap DAG tasks to container execution (DockerOperator locally then ECSOperator next)