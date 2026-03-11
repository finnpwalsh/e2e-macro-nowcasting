resource "aws_ecs_service" "this" {
    name            = var.name
    cluster         = var.cluster_arn
    task_definition = aws_ecs_task_definition.this.arn
    desired_count   = var.desired_count
    launch_type     = "FARGATE"

    network_configuration {
        subnets          = var.subnet_ids
        security_groups  = var.security_group_ids
        assign_public_ip = var.assign_public_ip
    }
}