← [Back to Docker](../README.md)

# Service Images

Container images for long-running infrastructure services that support the ML pipeline.

Service images are kept separate from runtimes to isolate dependencies and avoid coupling infrastructure services to job execution environments.

---

## Contract

- Service images define long-running infrastructure only
- Services do not extend the shared base runtime image
- Services are started once and shared across multiple jobs
- Job execution happens exclusively in runtime images

## Layout

```
infra/docker/services/
  airflow/
  mlflow/
```

Each folder defines a single infrastructure service image.