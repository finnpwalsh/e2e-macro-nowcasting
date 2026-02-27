variable "project" {
    type = string
    default = "nowcasting"
}

variable "env" {
    type = string
    default = "dev"
}

variable "aws_region" {
    type = string
    default = "us-east-1"
}

variable "vpc_id" {
    type = string
}

variable "subnet_ids" {
    type = string
}