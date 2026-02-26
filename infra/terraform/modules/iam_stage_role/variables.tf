variable "project" { type = string }

variable "env" { type = string }

variable "role_name" { type = string }

variable "s3_read_bucket_arns" {
    type = list(string)
    default = []
}

variable "s3_write_bucket_arns" {
    type = list(string)
    default = []
}

variable "ssm_read_path_prefix" {
    type = string
    default = ""
}

variable "ssm_write_parameter_arns" {
    type = list(string)
    default = []
}

variable "secrets_read_secret_arns" {
    type = list(string)
    default = []
}