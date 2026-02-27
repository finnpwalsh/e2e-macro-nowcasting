variable "project" { type = string }
variable "env"     { type = string }

variable "stages"  {
    description = "Map of stage role configurations"
    type = map(object({
        s3_read_bucket_arns      = list(string)
        s3_write_bucket_arns     = list(string)
        ssm_read_path_prefix     = string
        ssm_write_parameter_arns = list(string)
        secrets_read_secret_arns = list(string)
    }))
}