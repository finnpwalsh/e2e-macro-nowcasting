from __future__ import annotations

import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.metrics import mean_squared_error

from src.models.baseline import make_ridge_pipeline

def train_ridge(
       infile: Path = Path("data/processed/fred_wide.parquet"),
       target: str = "CPIAUCSL",
       split_date: str = "2020-01-01",
       alpha: float = 1.0,
):
    # read
    df = pd.read_parquet(infile)
    
    # prep
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # split target + feats
    y = df[target]
    X = df.drop(columns=["date", target])

    # split train + validate
    train = df["date"] < split_date
    valid = df["date"] >= split_date

    # make + fit model
    model = make_ridge_pipeline(
        feature_cols = X.columns.to_list(),
        alpha=alpha,
    )
    model.fit(X[train], y[train])

    # predict + eval
    y_hat = model.predict(X[valid])
    rmse = float(np.sqrt(mean_squared_error(y[valid], y_hat))) # numpy to float

    metrics = {
        "rmse": rmse,
        "split_date": split_date,
        "alpha": float(alpha),
        "n_train": int(train.sum()),
        "n_valid": int(valid.sum()),
        "n_feats": len(X.columns),
        "target": target,
    }

    # for plotting / EDA
    preds = pd.DataFrame(
        {
            "date": df.loc[valid, "date"],
            "y": y[valid],
            "y_hat": y_hat,
        }
    )

    return model, metrics, preds
