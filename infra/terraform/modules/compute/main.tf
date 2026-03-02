# ------------------------------------------
# ECS Cluster
# ------------------------------------------
resource "aws_ecs_cluster" "this" {
    name = "${var.project}-${var.env}-cluster"
}

# ------------------------------------------
# CloudWatch Logs
# ------------------------------------------

resource "aws_cloudwatch_log_group" "svc" {
    name              = "/ecs/${var.project}/${var.env}/${var.service_name}"
    retention_in_days = var.log_retention_days
}

# ------------------------------------------
# ECR Repo
# ------------------------------------------

resource "aws_ecr_repository" "svc" {
    name                 = "${var.project}-${var.env}-${var.service_name}"
    image_tag_mutability = "MUTABLE"
    
    image_scanning_configuration {
        scan_on_push = true
    }
}