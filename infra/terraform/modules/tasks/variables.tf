variable "name" { type = string }

variable "cpu"    { type = number }
variable "memory" { type = number }

variable "execution_role_arn" { type = string }
variable "task_role_arn"      { type = string }
variable "container_image"    { type = string }

variable "command" {
  type    = list(string)
  default = null
}

variable "environment" {
  type    = map(string)
  default = {}
}

variable "secrets" {
  type    = map(string)
  default = {}
}

variable "container_port" {
  type    = number
  default = null
}

variable "log_group_name" { type = string }
variable "aws_region"     { type = string }

variable "log_stream_prefix" {
  type    = string
  default = "ecs"
}