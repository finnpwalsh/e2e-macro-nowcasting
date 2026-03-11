resource "aws_ecs_task_definition" "this" {
    for_each = var.tasks

    family                   = each.value.family
    network_mode             = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    
    cpu    = tostring(each.value.cpu)
    memory = tostring(each.value.memory)
    
    execution_role_arn = var.execution_role_arn
    task_role_arn      = var.task_role_arns[each.key]

    container_definitions = jsonencode([
        {
            name      = each.value.family
            image     = each.value.container_image
            essential = true

            command = each.value.command
            
            environment = [
                for k, v in each.value.environment : { name = k, value = v }
            ]
            secrets = [
                for k, arn in each.value.secrets : { name = k, valueFrom = arn }
            ]

            portMappings = (
                try (each.value.container_port, null) == null
                ? [] : [{
                    containerPort = each.value.container_port
                    hostPort      = each.value.container_port
                    protocol      = "tcp"
                }]
            )

            logConfiguration = {
                logDriver = "awslogs"
                options = {
                    awslogs-group         = var.log_group_names[each.key]
                    awslogs-region        = var.aws_region
                    awslogs-stream-prefix = each.value.family
                }
            }
        }
    ])
}