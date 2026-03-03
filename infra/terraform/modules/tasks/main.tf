resource "aws_ecs_task_definition" "this" {
    family                   = var.name
    network_mode             = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    
    cpu    = tostring(var.cpu)
    memory = tostring(var.memory)
    
    execution_role_arn = var.execution_role_arn
    task_role_arn      = var.task_role_arn

    container_definitions = jsonencode([
        {
            name      = var.name
            image     = var.container_image
            essential = true

            command = var.command
            
            environment = [
                for k, v in var.environment : { name = k, value = v }
            ]
            secrets = [
                for k, arn in var.secrets : { name = k, valueFrom = arn }
            ]

            portMappings = var.container_port == null ? [] : [
                {
                    containerPort = var.container_port
                    hostPort      = var.container_port
                    protocol      = "tcp"
                }
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