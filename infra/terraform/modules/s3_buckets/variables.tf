variable "aws_region" {
  description = "AWS region for infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Project name prefix"
  type        = string
  default     = "nowcasting"
}

variable "env" {
  description = "Environment name (dev | prod)"
  type        = string
  default     = "dev"
}