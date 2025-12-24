"""
Train a baseline Ridge model on wide-form FRED time-series data.

This module takes clean, wide-form FRED data, feeds it to 
the baseline ridge model, and outputs the model, metrics, and
predictions.

Input Schema (wide-form):
- date (datetime)
- indicator_1 (numeric)
- indicator_2 (numeric)
- ...
- indicator_n (numeric)

Output:
- model (sklearn.pipeline.Pipeline): trained model
- metrics (dict): evaluation metrics and run metadata including:
    - regression performance metrics (e.g. RMSE, MAE, R2)
    - train/validation split info
    - model hyperparams
    - dataset dimensions
- preds (pd.DataFrame): model predictions with columns:
    - date (datetime64[ns])
    - y (float): observed target value
    - y_hat (float): model predictions

Called by scripts/train_ridge.py.
"""
from __future__ import annotations

import pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline

from src.models.baseline import make_ridge_pipeline
from src.evaluation.metrics import regression_metrics

def train_ridge(
       infile: Path = Path("data/processed/fred_wide.parquet"),
       target: str = "CPIAUCSL",
       split_date: str = "2020-01-01",
       alpha: float = 1.0,
) -> tuple[Pipeline, dict, pd.DataFrame]:
    """
    Train and evaluate a baseline Ridge regression model.

    Returns the fitted model, eval metrics, and a DataFrame
    of out-of-sample predictions.
    """
    # read
    df = pd.read_parquet(infile)
    
    # prep
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # drop rows w missing target
    df = df.dropna(subset=[target]).copy()

    # split target + feats
    y = df[target]
    X = df.drop(columns=["date", target])

    # split train + validate
    train = df["date"] < split_date
    valid = df["date"] >= split_date

    # make + fit model
    model = make_ridge_pipeline(alpha=alpha)
    model.fit(X[train], y[train])

    # predict + eval
    y_hat = model.predict(X[valid])
    metrics = regression_metrics(y[valid], y_hat)

    # add context to metrics
    metrics.update(
        {
        "split_date": split_date,
        "alpha": float(alpha),
        "n_train": int(train.sum()),
        "n_valid": int(valid.sum()),
        "n_feats": len(X.columns),
        "target": target,
        }
    )
    # for plotting / EDA
    preds = pd.DataFrame(
        {
            "date": df.loc[valid, "date"],
            "y": y[valid],
            "y_hat": y_hat,
        }
    )

    return model, metrics, preds
