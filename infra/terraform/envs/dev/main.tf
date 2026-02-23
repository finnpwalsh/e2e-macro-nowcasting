module "ssm_config" {
  source  = "../../modules/ssm_parameters"
  project = "nowcasting"
  env     = "dev"

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

module "secrets" {
  source  = "../../modules/secrets"
  project = "nowcasting"
  env     = "dev"

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