output "task_role_arns" {
    value = { for k, r in aws_iam_role.task : k => r.arn }
}

output "task_role_names" {
    value = { for k, r in aws_iam_role.task : k => r.name }
}

output "ecr_repo_urls" {
    value = { for k, r in aws_ecr_repository.task : k => r.repository_url }
}

output "log_group_arns" {
    value = { for k, lg in aws_cloudwatch_log_group.task : k => lg.arn }
}

output "log_group_names" {
    value = { for k, lg in aws_cloudwatch_log_group.task : k => lg.name }
}