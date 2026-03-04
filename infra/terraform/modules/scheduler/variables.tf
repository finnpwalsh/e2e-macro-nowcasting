variable "project" { type = string }
variable "env"     { type = string }

variable "state_machine_arns"   { type = map(string) }
variable "schedule_expressions" { type = map(string) }