← [Back to Docs](../README.md)

# Infrastructure

Cloud infrastructure powering the nowcasting platform.

---

## Environments

| Environment | Description |
| ----------- | ----------- |
| **dev** | development and testing environment |
| **prod** | production execution environment |

---

## Workflow

The platform executes scheduled ML pipelines using managed AWS services.

```
    Scheduler (EventBridge)
              ↓
 Orchestration (Step Functions)
              ↓
     ECS Tasks (Fargate)
              ↓
   S3 (datasets + artifacts)
```

---

## Core services

| Service | Purpose |
| ------- | ------- |
| **ECR** | container image registry |
| **ECS Fargate** | Serverless compute for containerized pipeline jobs |
| **EventBridge** | scheduled triggers for pipeline execution |
| **IAM** | runtime permissions and access control |
| **S3** | dataset and artifact storage |
| **Step Functions** | workflow orchestration for pipeline stages |
| **VPC** | network environment for ECS tasks and services |