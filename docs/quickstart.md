← [Back to Docs](../README.md)

# Quickstart

This guide explains how to run the full nowcasting pipeline via AWS.

---

## System Boot Flow

Booting the platform follows these steps:

```
Clone repository
      ↓
Authenticate with AWS
      ↓
Deploy infrastructure
      ↓
Configure API tokens
      ↓
Build and push runtime images
      ↓
Verify system execution
```

---

## Prerequisites

| Tool | Purpose |
| ---- | ------- |
| **Git** | Clone the repository |
| **Docker + Docker Compose** | Build and push container images |
| **Make** | Convenience commands for common workflows |
| **Terraform** | Provision cloud infrastructure |
| **AWS CLI v2** | Authenticate and interact with AWS |
| **AWS account access** | Permissions to deploy infrastructure |

---

## API Tokens 

| Token | Purpose | Get one |
| ----- | ------- | ------- |
| **FRED API key** | Access FRED macroeconomic data | [here](https://fred.stlouisfed.org/docs/api/api_key.html) |
| **Tiingo API token** | Access Tiingo market data | [here](https://www.tiingo.com/account/api/token) |

---

## 1. Clone Repository

```bash
git clone https://github.com/finnpwalsh/e2e-macro-nowcasting.git
cd e2e-macro-nowcasting
```

---

## 2. Authenticate with AWS

```bash
aws sso login --profile <your-profile>
```

---

## 3. Deploy infrastructure

```bash
cd infra/terraform/envs/dev
AWS_PROFILE=<your-profile> terraform init
AWS_PROFILE=<your-profile> terraform apply
```

---

## 4. Configure API tokens

Set tokens in `.env`:

```
FRED_API_KEY=<your-key>
TIINGO_API_TOKEN=<your-token>
```

---

## 5. Build and push runtime images

```bash
make build-runtimes
make push-runtimes
```

---

## 6. Verify system execution

The scheduler automatically trigges the pipeline via EventBridge.

You can monitor execution in:

- **Step Functions** – workflow executions
- **CloudWatch** – ECS task logs
- **S3** – datasets and artifacts

> You can manually trigger state machines inside AWS Console via Step Functions.