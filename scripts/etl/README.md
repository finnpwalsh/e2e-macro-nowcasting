# etl/
ETL scripts are responsible for producing **raw** and **processed** datasets and assembling **model-ready** training tables.


## `etl/anchors/` and `etl/shocks/`
*Sources-specific jobs (raw boundary + processed features)*

  - Each source owns its own ingestion and processed feature artifacts.
  - Source types: 
    - `anchors`: monthly macroeconomic data
    - `shocks`: intra-daily financial market tickers
  - Pattern:
    - `ingest.py` → writes raw source data
    - `build_wide.py` (or `build_<freq>_features.py`) → writes processed feature tables

---


## `etl/assemble/`
*cross-source assembly / alignment jobs*

  - Combines source-level processed artifacts into a **model-ready dataset** used by training.
  - In V1 this is typically a monthly dataset builder (may be a pure “merge” today).
  - In V2 this is where frequency alignment can live (monthly anchors + intraday sensors), while keeping training scripts stable.

---


## Example structure
```
etl/
  anchors/
    fred/
      ingest.py
      build_wide.py
  shocks/
    yfinance/
      ingest.py
      build_wide.py
  assemble/
    monthly.py        # V1: build model-ready monthly dataset
```

---