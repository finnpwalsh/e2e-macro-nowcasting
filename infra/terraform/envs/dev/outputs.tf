# -----------------------------------------------------
# ID / Env
# -----------------------------------------------------

output "project" { value = var.project }
output "env" { value = var.env }

output "aws_region" { value = data.aws_region.current.id }
output "aws_account_id" { value = data.aws_caller_identity.current.account_id }

# -----------------------------------------------------
# Storage
# -----------------------------------------------------

output "bucket_names" { value = module.storage.bucket_names }
output "bucket_arns" { value = module.storage.bucket_arns }

# -----------------------------------------------------
# Config
# -----------------------------------------------------

output "ssm_config_prefix" { value = local.ssm_config_prefix }

output "image_tag" {
  value     = data.aws_ssm_parameter.image_tag.value
  sensitive = true
}
output "secret_arns" {
  value     = module.config.secret_arns
  sensitive = true
}

# -----------------------------------------------------
# Runtime Platform
# -----------------------------------------------------

output "ecr_repo_urls" { value = module.runtimes.ecr_repo_urls }
output "runtime_role_arns" { value = module.runtimes.runtime_role_arns }
output "log_group_names" { value = module.runtimes.log_group_names }

# -----------------------------------------------------
# Compute
# -----------------------------------------------------

output "execution_role_arn" { value = module.compute.execution_role_arn }

# -----------------------------------------------------
# Tasks
# -----------------------------------------------------

output "task_definition_arns" { value = module.tasks.task_definition_arns }

# -----------------------------------------------------
# Network
# -----------------------------------------------------

output "vpc_id"                { value = module.network.vpc_id }
output "public_subnets"        { value = module.network.public_subnet_ids }
output "svc_security_group_id" { value = module.network.svc_security_group_id }

# -----------------------------------------------------
# Orchestration
# -----------------------------------------------------

output "state_machine_arns" { value = module.orchestration.state_machine_arns }