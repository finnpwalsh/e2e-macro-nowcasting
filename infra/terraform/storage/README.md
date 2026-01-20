← [Back to Terraform](../README.md)

# Storage

Cloud storage infrastructure used by the project.

---

## Contract

- Defines storage resources only
- Shared across multiple pipeline stages and services
- Does not contain application or execution logic

---

## Layout

```
storage/
  s3/
```