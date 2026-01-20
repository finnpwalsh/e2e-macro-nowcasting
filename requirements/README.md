# Requirements

Role-scoped dependency files for each stage of the ML lifecycle.

Designed for layered Docker runtimes:

- `base.txt` = shared deps installed in the base image
- `runtimes/*.txt` = incremental staged deps installed on top of base
- `dev/*.txt` = local/CI tooling (never used in production images)

---

## Contract

- `Production images must not install `requirements/dev/*`
- `requirements/runtimes/*.txt` must not include `-r ../base.txt` (shared deps come from the base image)
- Airflow uses a separate runtime (official `apache/airflow` image) and keeps deps isolated in `runtimes/airflow.txt``

---

## Layout

```
requirements/
  base.txt
  runtimes/
  dev/
```