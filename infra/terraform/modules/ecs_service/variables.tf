variable "name"               { type = string }

variable "cluster_arn"        { type = string }
variable "subnet_ids"         { type = list(string) }
variable "security_group_ids" { type = list(string) }

variable "execution_role_arn" { type = string }
variable "task_role_arn"      { type = string }

variable "container_image"    { type = string }
variable "container_port"     { type = number }

variable "command" {
    type = list(string)
    default = null
}

variable "environment" {
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

variable "cpu" {
    type = number
    default = 512
}

variable "memory" {
    type = number
    default = 1024
}

variable "desired_count" {
    type = number
    default = 1 
}