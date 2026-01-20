BASELINE_TRAIN_PRED_COLS = [
    "date",
    "y",
    "y_hat",
]

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

BASELINE_RUN_REQUIRED_KEYS = REGRESSION_METRICS + RUN_METADATA_KEYS