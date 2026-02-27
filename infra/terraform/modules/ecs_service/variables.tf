variable "name"               { type = string }

variable "cluster_arn"        { type = string }
variable "subnet_ids"         { type = string }
variable "security_group_ids" { type = string }

variable "execution_role_arn" { type = string }
variable "task_role_arn"      { type = string }

variable "container_image"    { type = string }
variable "container_port"     { type = number }

variable "command" {
    type = list(string)
    default = null
}

variable "env" {
    type = map(string)
    default = {}
}

variable "secrets" {
    type = map(string)
    default = {}
}

variable "log_group_name" { type = string }
variable "aws_region"     { type = string }

variable "assign_public_ip" {
    type    = bool
    default = true
}

variable "cpu" { type = number, default = 512 }
variable "memory" { type = number, default = 1024 }