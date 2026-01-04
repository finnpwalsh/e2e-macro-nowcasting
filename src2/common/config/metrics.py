REGRESSION_METRICS = [
    "rmse", 
]

RUN_METADATA_KEYS = [
    "split_date", 
    "n_train", 
    "n_valid", 
    "n_feats",
    "target",
]

TRAIN_RIDGE_REQUIRED_KEYS = REGRESSION_METRICS + RUN_METADATA_KEYS