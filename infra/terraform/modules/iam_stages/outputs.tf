output "role_arns" {
    value = { for k, m in module.stage : k => m.role_arn }
}

output "role_name" {
    value = { for k, m in module.stage : k => m.role_name }
}