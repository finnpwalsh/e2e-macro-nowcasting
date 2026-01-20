← [Back to Root](../README.md)

# Orchestration

Controls **when** pipeline stages run and **in what order**.

---

## Contract

Orchestration is intentionally thin.

It is responsible only for **wiring**:
- execution order
- dependencies
- scheduling

All implementation, logic, and I/O live elsewhere.

---

## Layout

```
orchestration/
  airflow/dags/
```