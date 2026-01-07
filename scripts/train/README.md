# train/
Training scripts produce **canonical model artifacts** and evaluation outputs. They should be **MLflow-free** (tracking is a separate step).


## `train/baseline/`
*slow-moving anchor model training (monthly macro)*

  - Implementation may change (ridge → elastic net → state space), but the *role* stays “baseline”.
  - Outputs: model file, metrics, predictions, `run.json` (and optionally residuals later)

---


## `train/residual/` (V2+)
*fast residual/corrector model training (intraday sensors)*

  - Trains a second model on baseline residuals (or deltas) using high-frequency features.

---


## `train/evaluate/` (optional, V2+) 
*model comparison/backtesting utilities*

  - Walk-forward backtests, leaderboard generation, selection logic (if you decide to separate it from `train.py`).

---


## Example structure
```
train/
  baseline/
    train.py
  residual/
    train.py
  evaluate/
    backtest.py
```