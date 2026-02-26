variable "project" {
    type = string
}

variable "env" {
    type = string
}

variable "role_name" {
    type = string
    default = "runtime"
}

variable "s3_read_bucket_arns" {
    description = "Bucket ARNs, not object ARNs. E.g.: arn:aws:s3::my-bucket"
    type = list(string)
}

variable "ssm_read_path_prefix" {
    description = "Leading slash prefix. E.g.: /myproj/dev/config/"
    type = string
}

variable "secrets_read_secret_arns" {
    description = "Exact Secrets manager secrets allowed for GetSecretValue"
    type = list(string)
    default = []
}