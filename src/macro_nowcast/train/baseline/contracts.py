PREDICTION_COLS = ("date", "y", "y_hat")

REQUIRED_SCORERS = ("rmse", )

REQUIRED_CONTEXT_KEYS = (
    "target",
    "split_date",
    "features",
)

REQUIRED_METRICS_KEYS = REQUIRED_SCORERS + REQUIRED_CONTEXT_KEYS