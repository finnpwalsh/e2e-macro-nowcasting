output "ssm_parameter_arns" {
    value = {
        for k, p in aws_ssm_parameter.config :
        k => p.arn
    }
}

output "ssm_path_prefix" {
    value = local.base
}

output "secret_arns" {
    value = {
        for k, s in aws_secretsmanager_secret.secret :
        k => s.arn
    }
}

output "secret_names" {
    value = {
        for k, s in aws_secretsmanager_secret.secret :
        k => s.name
  }
}