# ------------------------------------------
# Trust policy
# ------------------------------------------

data "aws_iam_policy_document" "assume" {
    statement {
        effect = "Allow"

        principals {
            type = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }

        actions = ["sts:AssumeRole"]
    }
}

resource "aws_iam_role" "this" {
    name = "${var.project}-${var.env}-scheduler"
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

        resources = values(var.state_machine_arns)
    }
}

resource "aws_iam_policy" "this" {
    name   = "${var.project}-${var.env}-scheduler"
    policy = data.aws_iam_policy_document.policy.json
}

# ------------------------------------------
# Schedules
# ------------------------------------------

resource "aws_scheduler_schedule" "this" {
    for_each = var.schedules

    name       = "${var.project}-${var.env}-${each.key}"
    group_name = "default"

    schedule_expression = each.value.schedule_expression

    flexible_time_window { mode = "OFF" }

    target {
        arn = var.state_machine_arns[each.value.machine]
        role_arn = aws_iam_role.this.arn
    }
}