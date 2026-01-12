# Requirements

Role-specific dependency files for each stage of the ML lifecycle.

---

## `base.txt`
Shared runtime dependencies for all job containers.

Used by:
- ETL
- Train
- Track
- Serve

---

## `etl.txt`
Data ingestion and preprocessing.

Extends:
```
-r base.txt
```

---

## `train.txt`
Model training and evaluation.

Extends:
```
-r base.txt
```

---

## `track.txt`
Experiment tracking and model promotion.

Extends:
```
-r base.txt
```

---

## `serve.txt`
Online inference.

Extends:
```
-r base.txt
```

---

## `airflow.txt`
Airflow scheduler/webserver dependencies only.

Notes:
- Does **not** extend `base.txt`
- No ML or application runtime deps

---

## `dev.txt`
Local development and CI utilities.

Notes:
- Union of job dependencies
- Not used to build production images