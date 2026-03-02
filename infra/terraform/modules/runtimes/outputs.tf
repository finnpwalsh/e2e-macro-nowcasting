output "runtime_role_arns" {
    value = { for k, r in aws_iam_role.runtime : k => r.arn }
}

output "runtime_role_names" {
    value = { for k, r in aws_iam_role.runtime : k => r.name }
}

output "ecr_repo_urls" {
    value = { for k, r in aws_ecr_repository.runtime : k => r.repository_url }
}

output "log_group_arns" {
    value = { for k, lg in aws_cloudwatch_log_group.runtime : k => lg.arn }
}

output "log_group_names" {
    value = { for k, lg in aws_cloudwatch_log_group.runtime : k => lg.name }
}