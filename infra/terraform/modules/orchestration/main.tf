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
            "ecs:StopTask",
        ]

        resources = ["*"]
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

    statement {
        sid    = "ManagedRuleForEcsSync"
        effect = "Allow"

        actions = [
            "events:PutRule",
            "events:PutTargets",
            "events:DescribeRule",
        ]

        resources = ["*"]
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
# State machines
# ------------------------------------------

resource "aws_sfn_state_machine" "this" {
    for_each   = var.machines
    name       = "${var.project}-${var.env}-${each.key}"
    role_arn   = aws_iam_role.this.arn
    definition = each.value.definition
}