← [Back to Infra](../README.md)

# Terraform

Infrastructure definitions for cloud resources used by the project.

---

## Contract

- `terraform/` defines how cloud resources are created and configured
- It does not contain application or business logic
- Resources are managed declaratively and versioned with the codebase

---

## Layout

```
infra/terraform/
  storage/
  serving/
```
