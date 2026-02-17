from __future__ import annotations

import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

def regression_metrics(
        y: pd.Series,
        y_pred: pd.Series | np.ndarray,
) -> dict[str, float]:
    """
    Computes regression metrics for model evaluation.

    Args:
        y: observed target values
        y_pred: predicted values
    
    Returns:
        dict[str, float]: regression metrics
            - rmse
            - mae
            - r2
            - mape
    """
    y = np.asarray(y)
    y_pred = np.asarray(y_pred)

    rmse = float(np.sqrt(mean_squared_error(y, y_pred)))
    mae = float(mean_absolute_error(y, y_pred))
    r2 = float(r2_score(y, y_pred))

    mape = float(np.mean(np.abs((y-y_pred) / y)) * 100)

    return {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "mape": mape,
    }