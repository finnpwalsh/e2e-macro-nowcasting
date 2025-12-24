from __future__ import annotations

import pandas as pd
import numpy as np
from pathlib import Path

from src.pipelines.baseline import train_ridge

REQUIRED_METRICS = ["rmse", "split_date", "n_train", "n_valid", "n_feats"]
REQUIRED_COLS = ["date", "y", "y_hat"]

def test_train_ridge(tmp_path: Path):
    # create df with NaN target val for testing
    df_in = pd.DataFrame(
        {
            "date": ["2019-11-01", "2019-12-01", "2020-01-01", "2020-02-01"],
            "CPIAUCSL": [100.0, 101.0, np.nan, 103.0],
            "feat1": [1.0, 2.0, 3.0, 4.0],
            "feat2": [10.0, 11.0, 12.0, 13.0],
        }
    )
    df_in["date"]=pd.to_datetime(df_in["date"])

    # temporary path created by pytest
    infile = tmp_path / "fred_wide_test.parquet"
    df_in.to_parquet(infile, index=False)

    # train w defaults
    model, metrics, preds = train_ridge(infile=infile)

    # check outputs exist
    assert isinstance(metrics, dict)
    assert isinstance(preds, pd.DataFrame)

    # check required metrics
    missing_mets = [c for c in REQUIRED_METRICS if c not in metrics.keys()]
    assert not missing_mets, f"Baseline ridge metrics json missing metrics: {missing_mets}"

    # check required cols
    missing_cols = [c for c in REQUIRED_COLS if c not in preds.columns]
    assert not missing_cols, f"Baseline ridge prediction df missing columns: {missing_cols}"