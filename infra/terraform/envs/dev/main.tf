# ========================================
# Locals
# ========================================

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  ssm_config_prefix = "/${var.project}/${var.env}/config/"
  ssm_champion_param_arn = "arn:aws:ssm:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:parameter${trimprefix(local.ssm_config_prefix, "/")}/champion"
}

# ========================================
# S3 Buckets
# ========================================

module "s3_buckets" {
  source = "../../modules/s3_buckets"

  project = var.project
  env = var.env
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
      s3_read_bucket_arns = [module.s3_buckets.data_bucket_arn]
      s3_write_bucket_arns = [module.s3_buckets.data_bucket_arn]
      ssm_read_path_prefix = local.ssm_config_prefix
      ssm_write_parameter_arns = []
      secrets_read_secret_arns = [
        module.secrets.arns["FRED_API_KEY"],
        module.secrets.arns["TIINGO_API_KEY"],
      ]
    }

    train = {
      s3_read_bucket_arns  = [module.s3_buckets.data_bucket_arn]
      s3_write_bucket_arns = [module.s3_buckets.artifacts_bucket_arn]
      ssm_read_path_prefix = local.ssm_config_prefix
      ssm_write_parameter_arns = []
      secrets_read_secret_arns = []
    }

    track = {
      s3_read_bucket_arns  = [module.s3_buckets.artifacts_bucket_arn]
      s3_write_bucket_arns = []
      ssm_read_path_prefix = local.ssm_config_prefix
      ssm_write_parameter_arns = []
      secrets_read_secret_arns = [
        module.secrets.arns["MLFLOW_BACKEND_STORE_URI"],
      ]
    }

    select = {
      s3_read_bucket_arns  = [module.s3_buckets.artifacts_bucket_arn]
      s3_write_bucket_arns = []
      ssm_read_path_prefix = local.ssm_config_prefix
      ssm_write_parameter_arns = [local.ssm_champion_param_arn]
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