output "anchors_state_machine_arn" {
    value = aws_sfn_state_machine.anchors.arn
}

output "orchestration_role_arn" {
    value = aws_iam_role.this.arn
}