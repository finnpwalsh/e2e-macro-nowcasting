variable "name"               { type = string }

variable "cluster_arn"         { type = string }
variable "task_definition_arn" { type = string }

variable "subnet_ids"         { type = list(string) }
variable "security_group_ids" { type = list(string) }

variable "assign_public_ip" {
    type    = bool
    default = true
}

variable "desired_count" {
    type = number
    default = 1 
}