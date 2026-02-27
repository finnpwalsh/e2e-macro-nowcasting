resource "aws_cloudwatch_log_group" "airflow" {
    name = "/${var.project}/${var.env}/airflow"
    retention_in_days = var.retention_in_days
}

resource "aws_cloudwatch_log_group" "mlflow" {
    name = "/${var.project}/${var.env}/mlflow"
    retention_in_days = var.retention_in_days
}

resource "aws_cloudwatch_log_group" "stages" {
    name = "/${var.project}/${var.env}/stages"
    retention_in_days = var.retention_in_days
}