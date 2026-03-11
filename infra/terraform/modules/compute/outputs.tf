output "ecs_cluster_arn" {
    value = aws_ecs_cluster.this.arn
}

output "ecs_cluster_name" {
    value = aws_ecs_cluster.this.name
}

output "execution_role_arn" {
    value = aws_iam_role.execution.arn
}

output "execution_role_name" {
    value = aws_iam_role.execution.name
}