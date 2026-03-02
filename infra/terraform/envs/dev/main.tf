# ========================================
# Locals
# ========================================

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  ssm_config_prefix      = "/${var.project}/${var.env}/config"
  ssm_champion_param_arn = "arn:aws:ssm:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:parameter${local.ssm_config_prefix}/champion"
}

# ========================================
# VPC
# ========================================

module "vpc" {
  source = "../../modules/vpc"

  vpc_cidr = var.vpc_cidr
}

# ========================================
# S3 Buckets
# ========================================

module "s3_buckets" {
  source = "../../modules/s3_buckets"

  project    = var.project
  env        = var.env
  aws_region = var.aws_region
}

# ========================================
# SSM Parameters
# ========================================

module "ssm_config" {
  source  = "../../modules/ssm_parameters"
  project = var.project
  env     = var.env

  values = {
    MLFLOW_TRACKING_URI    = "http://mlflow:5000"
    MLFLOW_EXPERIMENT_NAME = "nowcasting"
    NOWCAST_REGISTRY_NAME  = "nowcasting-models"
    NOWCAST_MODEL_ALIAS    = "champion"
    STORAGE_BACKEND        = "S3"
    AIRFLOW_ADMIN_USERNAME = "admin"
    AIRFLOW_ADMIN_EMAIL    = "admin@example.com"
  }
}

# ========================================
# Secrets Manager
# ========================================

module "secrets" {
  source  = "../../modules/secrets"
  project = var.project
  env     = var.env

  keys = [
    "FRED_API_KEY",
    "TIINGO_API_KEY",
    "AIRFLOW__WEBSERVER__SECRET_KEY",
    "AIRFLOW__CORE__FERNET_KEY",
    "AIRFLOW_ADMIN_PASSWORD",
    "AIRFLOW_DB_URI",
    "MLFLOW_BACKEND_STORE_URI",
  ]
}

# ========================================
# IAM Stages
# ========================================

module "iam_stages" {
  source  = "../../modules/iam_stages"
  project = var.project
  env     = var.env

  stages = {
    prepare = {
      s3_read_bucket_arns      = [module.s3_buckets.data_bucket_arn]
      s3_write_bucket_arns     = [module.s3_buckets.data_bucket_arn]
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = []
      secrets_read_secret_arns = [
        module.secrets.arns["FRED_API_KEY"],
        module.secrets.arns["TIINGO_API_KEY"],
      ]
    }

    train = {
      s3_read_bucket_arns      = [module.s3_buckets.data_bucket_arn]
      s3_write_bucket_arns     = [module.s3_buckets.artifacts_bucket_arn]
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = []
      secrets_read_secret_arns = []
    }

    track = {
      s3_read_bucket_arns      = [module.s3_buckets.artifacts_bucket_arn]
      s3_write_bucket_arns     = []
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = []
      secrets_read_secret_arns = [
        module.secrets.arns["MLFLOW_BACKEND_STORE_URI"],
      ]
    }

    select = {
      s3_read_bucket_arns      = [module.s3_buckets.artifacts_bucket_arn]
      s3_write_bucket_arns     = []
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = [local.ssm_champion_param_arn]
      secrets_read_secret_arns = [
        module.secrets.arns["MLFLOW_BACKEND_STORE_URI"],
      ]
    }

    mlflow = {
      s3_read_bucket_arns      = [module.s3_buckets.artifacts_bucket_arn]
      s3_write_bucket_arns     = [module.s3_buckets.artifacts_bucket_arn]
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = []
      secrets_read_secret_arns = [
        module.secrets.arns["MLFLOW_BACKEND_STORE_URI"],
      ]
    }
  }
}

# ========================================
# ECR Repositories
# ========================================

module "ecr" {
  source = "../../modules/ecr_repositories"

  project = var.project
  env     = var.env

  repositories = [
    "base",
    "prepare",
    "train",
    "track",
    "select",
    "airflow",
    "mlflow",
    "serve"
  ]
}

# ========================================
# ECS
# ========================================

module "ecs_cluster" {
  source  = "../../modules/ecs_cluster"
  project = var.project
  env     = var.env
}

module "ecs_execution_role" {
  source  = "../../modules/ecs_execution_role"
  project = var.project
  env     = var.env
}

module "ecs_sg" {
  source  = "../../modules/ecs_security_groups"
  project = var.project
  env     = var.env
  vpc_id  = var.vpc_id
}

# ========================================
# CloudWatch
# ========================================

module "logs" {
  source  = "../../modules/cloudwatch_logs"
  project = var.project
  env     = var.env

  retention_in_days = 14
}

# ========================================
# ECS Service
# ========================================

module "mlflow_service" {
  source = "../../modules/ecs_service"

  name        = "${var.project}-${var.env}-mlflow"
  cluster_arn = module.ecs_cluster.cluster_arn

  subnet_ids         = var.subnet_ids
  security_group_ids = [module.ecs_sg.svc_sg_id]

  execution_role_arn = module.ecs_execution_role.role_arn
  task_role_arn      = module.iam_stages.role_arns["mlflow"]

  container_image = "${module.ecr.repository_urls["mlflow"]}:dev"
  container_port  = 5000

  secrets = {
    MLFLOW_BACKEND_STORE_URI = module.secrets.arns["MLFLOW_BACKEND_STORE_URI"]
  }

  command = [
    "bash",
    "-lc",
    "mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri \"$MLFLOW_BACKEND_STORE_URI\" --default-artifact-root \"s3://${module.s3_buckets.artifacts_bucket}/mlflow\""
  ]

  log_group_name   = module.logs.log_group_names["mlflow"]
  aws_region       = var.aws_region
  assign_public_ip = false
  desired_count    = 1

  cpu    = 512
  memory = 1024

  depends_on = [module.rds]
}

# ========================================
# RDS Postgres
# ========================================

module "rds" {
  source = "../../modules/rds_postgres"

  project    = var.project
  env        = var.env
  aws_region = var.aws_region

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  allowed_sg_id = module.ecs_sg.svc_sg_id

  username = "nowcasting"

  instance_class    = "db.t4g.micro"
  allocated_storage = 20
  engine_version    = "16.3"
  db_name           = "postgres"

  secrets = {
    AIRFLOW_DB_URI           = module.secrets.arns["AIRFLOW_DB_URI"]
    MLFLOW_BACKEND_STORE_URI = module.secrets.arns["MLFLOW_BACKEND_STORE_URI"]
  }
}