locals {
  log_groups = {
    airflow = "/${var.project}/${var.env}/airflow"
    mlflow  = "/${var.project}/${var.env}/mlflow"
    stages  = "/${var.project}/${var.env}/stages"
  }
}

resource "aws_cloudwatch_log_group" "this" {
  for_each = local.log_groups

  name              = each.value
  retention_in_days = var.retention_in_days
}