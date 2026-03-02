output "data_bucket" {
  value = aws_s3_bucket.data.bucket
}

output "artifacts_bucket" {
  value = aws_s3_bucket.artifacts.bucket
}

output "airflow_logs_bucket" {
  value = aws_s3_bucket.airflow_logs.bucket
}

output "data_bucket_arn" {
  value = aws_s3_bucket.data.arn
}

output "artifacts_bucket_arn" {
  value = aws_s3_bucket.artifacts.arn
}

output "airflow_logs_bucket_arn" {
  value = aws_s3_bucket.airflow_logs.arn
}