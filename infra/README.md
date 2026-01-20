← [Back to Root](../README.md)

# Infra

Infrastructure definitions and runtime packaging for the project.

---

## Contract

- `infra/` defines infrastructure and runtime concerns only
- Application and modeling logic live outside `infra/`
- Infrastructure is declarative and environment-agnostic

---

## Layout

```
infra/
  docker/
  postgres/
  terraform/
```

- **[Docker](./docker/README.md)** – container images (runtimes + services)
- **[Postgres](./postgres/README.md)** – database initialization and schemas
- **[Terraform](./terraform/README.md)** – cloud infrastructure definitions