locals {
    name_prefix = "${var.project}-${var.env}"

    network_configuration = {
        AWSvpcConfiguration = {
            Subnets = var.subnet_ids
            SecurityGroups = var.security_group_ids
            AssignPublicIp = var.assign_public_ip ? "ENABLED" : "DISABLED"
        }
    }
}

# ------------------------------------------
# Trust policy
# ------------------------------------------

data "aws_iam_policy_document" "assume" {
    statement {
        effect = "Allow"

        principals {
            type        = "Service"
            identifiers = ["states.amazonaws.com"]
        }

        actions = ["sts:AssumeRole"]
    }
}

resource "aws_iam_role" "this" {
    name               = "${var.project}-${var.env}-orchestration"
    assume_role_policy = data.aws_iam_policy_document.assume.json
}

# ------------------------------------------
# ECS policy
# ------------------------------------------

data "aws_iam_policy_document" "policy" {
    statement {
        sid    = "RunTasks"
        effect = "Allow"

        actions = [
            "ecs:RunTask",
            "ecs:DescribeTasks",
        ]

        resources = [*]
    }

    statement {
        sid    = "PassRoles"
        effect = "Allow"

        actions = [
            "iam:PassRole"
        ]

        resources = concat(
            [var.execution_role_arn],
            values(var.task_role_arns)
        )
    }
}

resource "aws_iam_policy" "this" {
    name   = "${var.project}-${var.env}-orchestration"
    policy = data.aws_iam_policy_document.policy.json
}

resource "aws_iam_role_policy_attachment" "this" {
    role       = aws_iam_role.this.name
    policy_arn = aws_iam_policy.this.arn
}

# ------------------------------------------
# Anchors State Machine
# ------------------------------------------
locals {
        anchors_definiton = jsonencode({
        StartAt = "AnchorsIngestFred"
        States  = {
            AnchorsIngestFred = {
                Type = "Task"
                Resource = "arn:aws:states:::ecs:runTask.sync"
                Parameters = {
                    Cluster = var.ecs_cluster_arn
                    LaunchType = "FARGATE"
                    TaskDefinition = var.task_definition_arns["prepare"]
                    Overrides = {
                        ContainerOverrides = [{
                            Name    = "${local.name_prefix}-prepare"
                            Command = ["python", "-m", "prepare.anchors.sources.fred"]
                        }]
                    }
                }
                Next = "AnchorsAssemble"
            }

            AnchorsAssemble = {
                Type = "Task"
                Resource = "arn:aws:states:::ecs:runTask.sync"
                Parameters = {
                    Cluster = var.ecs_cluster_arn
                    LaunchType = "FARGATE"
                    TaskDefinition = var.task_definition_arns["prepare"]
                    Overrides = {
                        ContainerOverrides = [{
                            Name    = "${local.name_prefix}-prepare"
                            Command = ["python", "-m", "jobs.prepare.anchors.assemble"]
                        }]
                    }
                }
                Next = "AnchorsBuildFeatures"
            }

            AnchorsBuildFeatures = {
                Type = "Task"
                Resource = "arn:aws:states:::ecs:runTask.sync"
                Parameters = {
                    Cluster = var.ecs_cluster_arn
                    LaunchType = "FARGATE"
                    TaskDefinition = var.task_definition_arns["prepare"]
                    Overrides = {
                        ContainerOverrides = [{
                            Name    = "${local.name_prefix}-prepare"
                            Command = ["python", "-m", "jobs.prepare.anchors.build_features"]
                        }]
                    }
                }
                Next = "TrainBaseline"
            }

            TrainBaseline = {
                Type = "Task"
                Resource = "arn:aws:states:::ecs:runTask.sync"
                Parameters = {
                    Cluster = var.ecs_cluster_arn
                    LaunchType = "FARGATE"
                    TaskDefinition = var.task_definition_arns["train"]
                    Overrides = {
                        ContainerOverrides = [{
                            Name    = "${local.name_prefix}-train"
                            Command = ["python", "-m", "jobs.train.baseline"]
                        }]
                    }
                }
                Next = "PromoteChampion"
            }

            PromoteChampion = {
                Type = "Task"
                Resource = "arn:aws:states:::ecs:runTask.sync"
                Parameters = {
                    Cluster = var.ecs_cluster_arn
                    LaunchType = "FARGATE"
                    TaskDefinition = var.task_definition_arns["select"]
                    Overrides = {
                        ContainerOverrides = [{
                            Name    = "${local.name_prefix}-select"
                            Command = ["python", "-m", "jobs.select.promote"]
                        }]
                    }
                }
                End = true
            }
        }
    })
}

# ------------------------------------------
# Step Functions definition
# ------------------------------------------

resource "aws_sfn_state_machine" "anchors" {
    name       = "${local.name_prefix}-anchors"
    role_arn   = aws_iam_role.this.arn
    definition = local.anchors_definition
}