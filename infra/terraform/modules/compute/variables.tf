variable "project"      { type = string }
variable "env"          { type = string }
variable "aws_region"   { type = string }
variable "service_name" { type = string }

variable "log_retention_days" {
    type = number
    default = 7
}
