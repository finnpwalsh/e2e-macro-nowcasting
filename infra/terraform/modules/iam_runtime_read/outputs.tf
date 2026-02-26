output "task_role_name" {
    value = aws_iam_role.task.name
}

output "task_role_arn" {
    value = aws_iam_role.task.arn
}

output "policy_arn" {
    value = aws_iam_policy.runtime_read.arn
}