variable "project"    { type = string }
variable "env"        { type = string }
variable "aws_region" { type = string }

variable "cluster_arn"          { type = string }
variable "execution_role_arn"   { type = string }
variable "task_definition_arns" { type = map(string) }
variable "task_role_arns"       { type = map(string) }

variable "subnet_ids"        { type = true }
variable "security_group_id" { type = string }

variable "assign_public_ip" {
    type = bool
    default = true
}