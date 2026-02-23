output "base_path" {
    value = local.base
}

output "names" {
    value = {for k, p in aws_ssm_parameters.this : k => p.name}
}