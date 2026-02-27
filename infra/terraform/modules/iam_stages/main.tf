module "stage" {
    source   = "../iam_task_roles"
    for_each = var.stages

    project   = var.project
    env       = var.env
    role_name = each.key

    s3_read_bucket_arns = each.value.s3_read_bucket_arns
    s3_write_bucket_arns = each.value.s3_write_bucket_arns
    ssm_read_path_prefix = each.value.ssm_read_path_prefix
    ssm_write_parameter_arns = each.value.ssm_write_parameter_arns
    secrets_read_secret_arns = each.value.secrets_read_secret_arns
}