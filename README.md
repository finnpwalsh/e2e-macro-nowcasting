# End-to-End Macro Nowcasting

End-to-end inflation nowcasting system built as a production-grade ML platform emphasizing reproducibility and governed model lifecycle management.

This repository demonstrates how to design, version, evaluate and operate a macroeconomic ML system end-to-end, with explicit separation between infrastructure, modeling, and serving responsibilities. 

---

## Status
**Jan 19, 2026**: Under active development

**v1.4.0** released — full S3-backed storage integration

---

## Contents
- [Layout](#layout)
- [Documentation](#documentation)
- [Quickstart](#quickstart)

---

## Layout

```
├── docs/
├── infra/
├── jobs/
├── orchestration/
├── requirements/
├── src/
└── tests/
```

**Components**

- **Docs** – design and reference documents
- **[Infra](infra/docker/README.md)** – Docker and cloud infrastructure
- **[Jobs](jobs/README.md)** – Executable pipeline entrypoints
- **Orchestration** – Airflow DAGs
- **[Requirements](requirements/README.md)** – dependency specs
- **[Source](src/README.md)** – Reusable library code
- **Tests** – Automated checks

---

## Documentation

Deeper design, architecture, and planning documents:

- **[Architecture & System Design](docs/architecture.md)** – Overall V1 architecture, execution boundaries, and lifecycle contracts
- **[Roadmap & Version Planning](docs/roadmap.md)** – Planned scope for V1-V4 and future modeling/ops work
- **[Version History](docs/version-history.md)** – Tagged releases and major milestones

Working documentss:

- **[Development Log](docs/DEVLOG.md)** – chronological record of implementation progress and decisions
- **[Project Plan](docs/PLAN.md)** – near-term execution plan and task breakdown

---

## Quickstart

Docker is the source of truth for runtime behavior. The steps below run the full pipeline locally using Airflow and S3-backed storage.

### Prerequisites
- Docker + Docker Compose
- Make
- A FRED API key ([get one here](https://fred.stlouisfed.org/docs/api/api_key.html))

---

### Run
1. Clone the repository
```
git clone https://github.com/finnpwalsh/e2e-macro-nowcasting.git
cd e2e-macro-nowcasting
```

---

2. Configure environment variables
Copy the example file and fill in required values:

```
cp .env.example .env
```

At minimum, set:
`FRED_API_KEY` • `AIRFLOW__WEBSERVER__SECRET_KEY` • `AWS_S3_BUCKET_DATA` • `AWS_S3_BUCKET_ARTIFACTS` • `AWS_S3_REGION` • `AWS_PROFILE`

---

3. Build Containers
```
make build
```

---

4. Start Airflow
``` 
make up
```

Access the Airflow UI at: http://localhost:8080
**Login**: Username: `admin` | Password: `admin`

Access the MLflow UI at: http://localhost:5000

---

5. Run the pipeline
```
make run
```

This executes the full pipeline end-to-end.

---

6. Shut down

```
make down
```

---

### Run individual stages

These targets run individual pipeline stages inside containers without requiring a full DAG execution.

- `make ingest`
- `make clean`
- `make train`
- `make merge`
- `make test` (data contract testing via pytest)