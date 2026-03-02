locals {
    name_prefix = "${var.project}-${var.env}"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [{
        Effect = "Allow"
        Principal = {
            Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
        }]
    })
}

# ----------------------------------------------------------
# ECS Cluster
# ----------------------------------------------------------

resource "aws_ecs_cluster" "this" {
    name = "${local.name_prefix}-cluster"
}

# ----------------------------------------------------------
# ECS Execution Role
# ----------------------------------------------------------

resource "aws_iam_role" "execution" {
    name               = "${local.name_prefix}-ecs-execution"
    assume_role_policy = local.assume_role_policy
}

# ----------------------------------------------------------
# Execution Role Policy
# ----------------------------------------------------------

data "aws_iam_policy_document" "execution" {

    statement {
        sid     = "ECRPull"
        effect  = "Allow"
        actions = [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
        ]
        resources = ["*"]
    }

    statement {
        sid     = "CloudWatchLogs"
        effect  = "Allow"
        actions = [
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ]
        resources = ["*"]
    }

    statement {
        sid     = "SecretsReadAtLaunch"
        effect  = "Allow"
        actions = [
            "secretsmanager:GetSecretValue"
        ]
        resources = ["*"]
    }
}

resource "aws_iam_policy" "execution" {
    name   = "${local.name_prefix}-ecs-execution-policy"
    policy = data.aws_iam_policy_document.execution.json
}

resource "aws_iam_role_policy_attachment" "execution" {
    role       = aws_iam_role.execution.name
    policy_arn = aws_iam_policy.execution.arn
}