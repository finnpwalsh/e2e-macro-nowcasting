variable "project" { type = string }
variable "env"     { type = string }

variable "ssm_parameters" { type = map(string) }
variable "secrets"        { type = set(string) }