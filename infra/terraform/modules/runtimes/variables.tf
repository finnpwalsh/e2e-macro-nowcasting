variable "project" { type = string }
variable "env"     { type = string }

variable "aws_region"     { type = string }
variable "aws_account_id" { type = string }

variable "log_retention_days" {
    type    = number
    default = 14
}

variable "runtimes" {
    type = map(object({
        s3_read_bucket_arns      = list(string)
        s3_write_bucket_arns     = list(string)
        ssm_read_path_prefix     = string
        ssm_write_parameter_arns = list(string)
        secrets_read_secret_arns = list(string)
    }))
}