← [Back to Terraform](../README.md)

# Serving

Cloud infrastructure for running online services (implemented v1.5.0).

---

## Contract

- Defines infrastructure required to run serving workloads
- Supports long-running services (e.g. FastAPI on ECS/Fargate)
- Does not contain application or business logic

---

## Layout (future)

```
serving/
  ecs/
  iam/
```