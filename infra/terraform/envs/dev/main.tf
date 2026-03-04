# ========================================
# Locals
# ========================================

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  ssm_config_prefix      = "/${var.project}/${var.env}/config"
  ssm_champion_param_arn = "arn:aws:ssm:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:parameter${local.ssm_config_prefix}/champion"
}

data "aws_ssm_parameter" "image_tag" {
  name       = "${local.ssm_config_prefix}/IMAGE_TAG"
  depends_on = [module.config]
}

locals {
  images = {
    prepare = "${module.runtimes.ecr_repo_urls["prepare"]}:${data.aws_ssm_parameter.image_tag.value}"
    train   = "${module.runtimes.ecr_repo_urls["train"]}:${data.aws_ssm_parameter.image_tag.value}"
    select  = "${module.runtimes.ecr_repo_urls["select"]}:${data.aws_ssm_parameter.image_tag.value}"
  }
}

# ========================================
# Storage
# ========================================

module "s3_buckets" {
  source  = "../../modules/storage"
  project = var.project
  env     = var.env

  aws_region = var.aws_region
}

# ========================================
# Config
# ========================================

module "config" {
  source  = "../../modules/config"
  project = var.project
  env     = var.env

  ssm_parameters = {
    STORAGE_BACKEND = "S3"
    IMAGE_TAG       = "v1.5.0"
  }

  secrets = [
    "FRED_API_KEY",
    "TIINGO_API_KEY",
  ]
}

# ========================================
# Compute
# ========================================

module "compute" {
  source  = "../../modules/compute"
  project = var.project
  env     = var.env
}

# ========================================
# Runtimes
# ========================================

module "runtimes" {
  source = "../../modules/runtimes"

  project = var.project
  env     = var.env

  aws_region     = data.aws_region.current.id
  aws_account_id = data.aws_caller_identity.current.account_id

  log_retention_days = 14

  runtimes = {
    prepare = {
      s3_read_bucket_arns      = [module.s3_buckets.data_bucket_arn]
      s3_write_bucket_arns     = [module.s3_buckets.data_bucket_arn]
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = []
    }

    train = {
      s3_read_bucket_arns      = [module.s3_buckets.data_bucket_arn]
      s3_write_bucket_arns     = [module.s3_buckets.artifacts_bucket_arn]
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = []
    }

    select = {
      s3_read_bucket_arns      = [module.s3_buckets.artifacts_bucket_arn]
      s3_write_bucket_arns     = []
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = [local.ssm_champion_param_arn]
    }
  }
}

# ========================================
# Tasks
# ========================================

module "tasks" {
  source = "../../modules/tasks"

  aws_region         = data.aws_region.current.id
  execution_role_arn = module.compute.execution_role_arn
  task_role_arns     = module.runtimes.runtime_role_arns
  log_group_names    = module.runtimes.log_group_names

  tasks = {
    prepare = {
      family          = "${var.project}-${var.env}-prepare"
      cpu             = 512
      memory          = 1024
      container_image = local.images["prepare"]
      command         = ["python", "-m", "jobs.prepare.run"]

      environment = {
        PROJECT           = var.project
        ENV               = var.env
        SSM_CONFIG_PREFIX = local.ssm_config_prefix
        STAGE             = "prepare"
      }

      secrets = {
        FRED_API_KEY   = module.config.secret_arns["FRED_API_KEY"]
        TIINGO_API_KEY = module.config.secret_arns["TIINGO_API_KEY"]
      }
    }

    train = {
      family          = "${var.project}-${var.env}-train"
      cpu             = 512
      memory          = 1024
      container_image = local.images["train"]
      command         = ["python", "-m", "jobs.train.run"]

      environment = {
        PROJECT           = var.project
        ENV               = var.env
        SSM_CONFIG_PREFIX = local.ssm_config_prefix
        STAGE             = "train"
      }

      secrets = {}
    }

    select = {
      family          = "${var.project}-${var.env}-select"
      cpu             = 512
      memory          = 1024
      container_image = local.images["select"]
      command         = ["python", "-m", "jobs.select.run"]

      environment = {
        PROJECT           = var.project
        ENV               = var.env
        SSM_CONFIG_PREFIX = local.ssm_config_prefix
        STAGE             = "select"
      }

      secrets = {}
    }
  }
}