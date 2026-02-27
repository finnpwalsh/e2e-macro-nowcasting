variable "project"    { type = string }
variable "env"        { type = string }
variable "aws_region" { type = string }

variable "vpc_id"  { type = string }
variable "subnet_ids" { type = list(string) }

variable "allowed_sg_id" { type = string }

variable "db_name" {
    type = string
    default = "postgres"
}
variable "username" {
    type = string
    default = "nowcasting"
}

variable "instance_class" {
    type = string
    default = "db.t4g.micro"
}

variable "allocated_storage" {
    type = number
    default = 20
}
variable "engine_version" {
    type = string
    default = "16.3"
}

variable "secrets" {
    type = map(string)
}