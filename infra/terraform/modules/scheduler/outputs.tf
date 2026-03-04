output "scheduler_role_arn" {
    value = aws_iam_role.this.arn
}

output "schedule_arns" {
    value = {
        anchors = aws_scheduler_schedule.anchors.arn
        shocks  = aws_scheduler_schedule.shocks.arn
    }
}