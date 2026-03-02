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
# Storage
# ========================================

module "s3_buckets" {
  source = "../../modules/storage"

  project    = var.project
  env        = var.env
  aws_region = var.aws_region
}

# ========================================
# Config
# ========================================

module "config" {
  source  = "../../modules/config"
  project = var.project
  env     = var.env

  ssm_parameters = {
    MLFLOW_TRACKING_URI    = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME = "nowcasting"
    NOWCAST_REGISTRY_NAME  = "nowcasting-models"
    NOWCAST_MODEL_ALIAS    = "champion"
    STORAGE_BACKEND        = "S3"
    AIRFLOW_ADMIN_USERNAME = "admin"
    AIRFLOW_ADMIN_EMAIL    = "admin@example.com"
  }

  secrets = [
    "FRED_API_KEY",
    "TIINGO_API_KEY",
    "AIRFLOW__WEBSERVER__SECRET_KEY",
    "AIRFLOW__CORE__FERNET_KEY",
    "AIRFLOW_ADMIN_PASSWORD",
  ]
}