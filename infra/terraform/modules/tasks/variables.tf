variable "aws_region" { type = string }

variable "execution_role_arn" { type = string }
variable "task_role_arns"     { type = map(string) }
variable "log_group_names"    { type = map(string) }

variable "tasks" {
  type = map(object({
    family          = string
    cpu             = number
    memory          = number
    container_image = string
    container_port  = optional(number)
    command         = list(string)

    environment = map(string)
    secrets     = map(string)
  }))
}