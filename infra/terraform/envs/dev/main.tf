module "ssm_config" {
    source = "../../modules/ssm_parameters"
    project = "nowcasting"
    env = "dev"
}

values = {
    MLFLOW_TRACKING_URI = "http://mlflow:5000"
    MLFLOW_EXPERIMENT_NAME = "nowcasting"
    NOWCAST_REGISTRY_NAME = "nowcasting-models"
    NOWCAST_MODEL_ALIAS = "champion"
    STORAGE_BACKEND = "S3"
}