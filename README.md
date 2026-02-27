# End-to-End Macro Nowcasting

End-to-end inflation nowcasting system built as a production-grade ML platform emphasizing reproducibility and governed model lifecycle management.

This repository demonstrates how to design, version, evaluate and operate a macroeconomic ML system end-to-end, with explicit separation between infrastructure, modeling, and serving responsibilities. 

> **Getting started**
> - See [`docs/README.md`](docs/README.md) for detailed project documentation
> - New here? See [Quickstart](docs/quickstart.md) to run the system locally

**Design Note:** Several components of the system are deliberately more elaborate than required for the current model in order to practice production-grade data, ML, and systems design patterns.

---

## Status

- **Latest release**: v1.4.0 – S3-backed storage
- **In progress**: v1.5.0 – execution & contract hardening

---

## Layout

```
├── docs/
├── infra/
├── jobs/
├── orchestration/
├── requirements/
├── src/
│   ├── ml_platform/
│   └── macro_nowcast/
└── tests/
```

**Components**

- **[Docs](docs/README.md)** – design and reference documents
- **[Infra](infra/docker/README.md)** – Docker and cloud infrastructure
- **[Jobs](jobs/README.md)** – Executable pipeline entrypoints
- **[Orchestration](orchestration/README.md)** – Airflow DAGs
- **[Requirements](requirements/README.md)** – dependency specs
- **[Source](src/README.md)** – Reusable library code
- **Tests** – Automated checks

> `ml_platform` contains reusable ML lifecycle and infrastructure, while `macro_nowcast` contains domain-specific inflation modeling code.