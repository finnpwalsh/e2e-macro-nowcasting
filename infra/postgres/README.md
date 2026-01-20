← [Back to Infra](../README.md)

# Postgres

PostgreSQL resources used by infrastructure and backend services.

---

## Contract

- `postgres/` defines how databases are created and initialized
- Application and business logic live outside `postgres/`
- Each service is responsible for managing its own database schema

---

## Layout

```
postgres/
  init/
```