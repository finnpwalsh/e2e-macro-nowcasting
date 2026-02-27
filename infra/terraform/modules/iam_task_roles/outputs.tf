output "role_name" { value = aws_iam_role.task.name }

output "role_arn" { value = aws_iam_role.task.arn }

output "policy_arn" { value = aws_iam_policy.stage.arn }