resource "aws_ecs_task_definition" "this" {
    family                   = var.name
    network_mode             = "awsvpc"
    required_compatabilities = ["FARGATE"]
    cpu                      = tostring(var.cpu)
    memory                   = tostring(var.memory)
    execution_role_arn       = var.execution_role_arn
    task_role_arn            = var.task_role_arn

    container_definitions = jsonencode([
        {
            name = var.name
            image = var.container_image
            essential = true
            portMappings = [
                {
                    container_port = var.container_port
                    hostPort       = var.container_port
                    protocol       = "tcp"
                }
            ]
            command = var.command
            environment = [
                for k, arn in var.env : { name = k, valueFrom = arn }
            ]
            secrets = [
                for k, arn in var.secrets : { name = k, valueFrom = arn }
            ]
            logConfiguration = {
                logDriver = "awslogs"
                options = {
                    awslogs-group         = var.log_group_name
                    awslogs-region        = var.aws_region
                    awslogs-stream-prefix = var.name
                }
            }
        }
    ])
}

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