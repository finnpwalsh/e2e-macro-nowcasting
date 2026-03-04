locals {
    name_prefix = "${var.project}-${var.env}"
}

# ------------------------------------------
# Trust policy
# ------------------------------------------

data "aws_iam_policy_document" "assume" {
    statement {
        effect = "Allow"

        principals {
            type = "Service"
            identifiers = ["schedulers.amazonaws.com"]
        }

        actions = ["sts:AssumeRole"]
    }
}

resource "aws_iam_role" "this" {
    name = "${local.name_prefix}-scheduler"
    assume_role_policy = data.aws_iam_policy_document.assume.json
}

# ------------------------------------------
# StartExecution policy
# ------------------------------------------

data "aws_iam_policy_document" "policy" {
    statement {
        sid    = "StartExecutions"
        effect = "Allow"

        actions = [
            "states:StartExecution",
        ]

        resources = [
            var.state_machine_arns["anchors"],
        ]
    }
}

resource "aws_iam_policy" "this" {
    name   = "${local.name_prefix}-scheduler"
    policy = data.aws_iam_policy_document.policy.json
}

# ------------------------------------------
# Schedules
# ------------------------------------------

resource "aws_scheduler_schedule" "anchors" {
    name = "${local.name_prefix}-anchors"
    group_name = "default"

    schedule_expression = var.schedule_expressions["anchors"]

    flexible_time_window { mode = "OFF" }

    target {
        arn = var.state_machine_arns["anchors"]
        role_arn = aws_iam_role.this.arn
    }
}