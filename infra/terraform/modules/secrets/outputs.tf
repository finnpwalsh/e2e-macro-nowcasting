output "base_path" {
    value = local.base
}

output "arns" {
    value = { for k, s in aws_secretsmanager_secret.this : k => s.arn }
}

output "names" {
    value = { for k, s in aws_secretsmanager_secret.this : k => s.name }
}