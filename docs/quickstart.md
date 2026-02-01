# Quickstart

This document includes how to run the full pipeline locally using Airflow and S3-backed storage.

## Prerequisites

- Docker + Docker Compose
- Make
- A FRED API key ([get one here](https://fred.stlouisfed.org/docs/api/api_key.html))

Docker is the source of truth for runtime behavior.

---

## Run
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

## Run individual stages

These targets run individual pipeline stages inside containers without requiring a full DAG execution.

- `make ingest`
- `make clean`
- `make train`
- `make merge`
- `make test` (data contract testing via pytest)