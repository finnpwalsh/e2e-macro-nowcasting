from __future__ import annotations

import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error

def regression_metrics(
        y: pd.Series,
        y_pred: np.ndarray,
) -> dict[str, float]:
    """
    Computes regression metrics for model evaluation.

    Args:
        y (pd.Series): observed target values
        y_pred (np.ndarray): predicted values
    
    Returns:
        dict[str, float]: regression metrics (currently incl. RMSE)
    """
    rmse = float(np.sqrt(mean_squared_error(y, y_pred)))

    return {
        "rmse": rmse,
    }
    