← [Back to Infra](../README.md)

# Terraform

Infrastructure definitions for cloud resources used by the project. 

Divided by production vs. development environment. Environments are responsible for all module instantiations.

---

## Modules

| Module | Description |
| ------ | ----------- |
| **compute** | ECS cluster and compute environment definitions |
| **config** | shared variables and secrets |
| **network** | VPC, subnets, and network infrastructure |
| **orchestration** | Step Functions workflows – orchestrate pipeline execution |
| **runtimes** | IAM roles and ECR repositories for pipeline tasks |
| **scheduler** | EventBridge schedules triggering pipeline workflows |
| **services** | Long-running services |
| **storage** | S3 buckets and storage infrastructure |
| **tasks** | ECS task definitions for pipeline jobs |

---

## Module interaction

- **orchestration** wires **tasks** into executable pipelines
- **scheduler** triggers **orchestration** workflows
- **tasks** run on **compute** (ECS/Fargate)
- **tasks** pull images from **runtimes** (ECR)
- **tasks** access **storage** (S3) using **runtimes** IAM roles
- **services** run persistent workloads on **compute**
- **network** provides infrastructure for **compute** and **services**