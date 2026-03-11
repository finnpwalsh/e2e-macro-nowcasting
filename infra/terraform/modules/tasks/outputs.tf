output "task_definition_arns" {
    value = { for k, v in aws_ecs_task_definition.this : k => v.arn }
}

output "task_definition_families" {
    value = { for k, v in aws_ecs_task_definition.this : k => v.family }
}