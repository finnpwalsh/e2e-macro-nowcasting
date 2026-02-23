output "base_path" {
    value = local.base
}

output "names" {
    value = {for k, p in aws_ssm_parameter.this : k => p.name}
}