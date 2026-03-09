output "state_machine_arns" {
    value = { for k, v in aws_sfn_state_machine.this : k => v.arn }
}