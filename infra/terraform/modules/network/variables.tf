variable "project" { type = string }
variable "env"     { type = string }

variable "vpc_cidr" {
    type    = string
    default = "10.20.0.0/16"
}

variable "svc_port" {
    type        = number
    default     = 8000
}