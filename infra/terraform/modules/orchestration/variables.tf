variable "project" { type = string }
variable "env"     { type = string }

variable "execution_role_arn"   { type = string }
variable "task_role_arns"       { type = map(string) }

variable "machines" { type = map(object({ definition = string })) }