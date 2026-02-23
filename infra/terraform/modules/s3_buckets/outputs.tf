output "data_bucket" {
  value = aws_s3_bucket.data.bucket
}

output "artifacts_bucket" {
  value = aws_s3_bucket.artifacts.bucket
}

output "airflow_logs_bucket" {
  value = aws_s3_bucket.airflow_logs.bucket
}