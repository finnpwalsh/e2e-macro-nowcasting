output "scheduler_role_arn" {
    value = aws_iam_role.this.arn
}

output "schedule_names" {
    value = {
        for k, v in aws_scheduler_schedule.this : k => v.name
    }
}