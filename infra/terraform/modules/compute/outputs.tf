output "ecs_cluster_arn" {
    value = aws_ecs_cluster.this.arn
}

output "ecs_cluster_name" {
    value = aws_ecs_cluster.this.name
}

output "log_group_name" {
    value = aws_cloudwatch_log_group.svc.name
}

output "ecr_repo_url" {
    value = aws_ecr_repository.svc.repository_url
}