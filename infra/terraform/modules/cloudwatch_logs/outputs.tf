output "airflow_log_group_name" { value = aws_cloudwatch_log_group.airflow.name }
output "mlflow_log_group_name"  { value = aws_cloudwatch_log_group.mlflow.name }
output "stages_log_group_name"  { value = aws_cloudwatch_log_group.stages.name }