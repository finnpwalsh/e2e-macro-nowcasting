variable "project" { type = string }
variable "env"     { type = string }

variable "state_machine_arns"   { type = map(string) }

variable "schedules" {
    type = map(object({
        machine             = string
        schedule_expression = string
    }))
}