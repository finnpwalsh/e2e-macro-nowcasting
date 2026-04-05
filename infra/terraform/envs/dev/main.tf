# ========================================
# Locals
# ========================================

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  ssm_config_prefix = "/${var.project}/${var.env}/config"
}

data "aws_ssm_parameter" "image_tag" {
  name       = "${local.ssm_config_prefix}/IMAGE_TAG"
  depends_on = [module.config]
}

locals {
  image_tag = data.aws_ssm_parameter.image_tag.value
  images = {
    prepare = "${module.runtimes.ecr_repo_urls["prepare"]}:${local.image_tag}"
    train   = "${module.runtimes.ecr_repo_urls["train"]}:${local.image_tag}"
    select  = "${module.runtimes.ecr_repo_urls["select"]}:${local.image_tag}"
  }
}

# ========================================
# Storage
# ========================================

module "storage" {
  source     = "../../modules/storage"
  project    = var.project
  env        = var.env
  aws_region = var.aws_region

  buckets = ["data", "artifacts"]
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
    IMAGE_TAG       = "v1.5.1"
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
      s3_read_bucket_arns      = [module.storage.bucket_arns["data"]]
      s3_write_bucket_arns     = [module.storage.bucket_arns["data"]]
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = []
    }

    train = {
      s3_read_bucket_arns      = [module.storage.bucket_arns["data"]]
      s3_write_bucket_arns     = [module.storage.bucket_arns["artifacts"]]
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = []
    }

    select = {
      s3_read_bucket_arns      = [module.storage.bucket_arns["artifacts"]]
      s3_write_bucket_arns     = [module.storage.bucket_arns["artifacts"]]
      ssm_read_path_prefix     = local.ssm_config_prefix
      ssm_write_parameter_arns = []
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

# ========================================
# Network
# ========================================

module "network" {
  source = "../../modules/network"

  project = var.project
  env     = var.env

  vpc_cidr = "10.0.0.0/16"
  svc_port = 8000
}

# ========================================
# Orchestration
# ========================================

locals {
  sfn_network_configuration = {
    AwsvpcConfiguration = {
      Subnets        = module.network.public_subnet_ids
      SecurityGroups = [module.network.svc_security_group_id]
      AssignPublicIp = "ENABLED"
    }
  }
}

module "orchestration" {
  source = "../../modules/orchestration"

  project = var.project
  env     = var.env

  execution_role_arn = module.compute.execution_role_arn
  task_role_arns     = module.runtimes.runtime_role_arns

  machines = {

    # -----------------------------------------
    # [ANCHORS][PREPARE]
    # -----------------------------------------

    anchors_prepare = {
      definition = jsonencode({
        StartAt = "PrepareAnchorsFred"
        States = {

          # ---------------------------------
          # [ANCHORS][PREPARE][FRED]
          # ---------------------------------

          PrepareAnchorsFred = {
            Type     = "Task"
            Resource = "arn:aws:states:::ecs:runTask.sync"
            Parameters = {
              Cluster              = module.compute.ecs_cluster_arn
              LaunchType           = "FARGATE"
              NetworkConfiguration = local.sfn_network_configuration

              TaskDefinition = module.tasks.task_definition_arns["prepare"]
              Overrides = {
                ContainerOverrides = [{
                  Name    = "${var.project}-${var.env}-prepare"
                  Command = ["python", "-m", "jobs.prepare.anchors.sources.fred"]
                }]
              }
            }
            Next = "AnchorsAssemble"
          }

          # ---------------------------------
          # [ANCHORS][PREPARE][ASSEMBLE]
          # ---------------------------------

          AnchorsAssemble = {
            Type     = "Task"
            Resource = "arn:aws:states:::ecs:runTask.sync"
            Parameters = {
              Cluster              = module.compute.ecs_cluster_arn
              LaunchType           = "FARGATE"
              TaskDefinition       = module.tasks.task_definition_arns["prepare"]
              NetworkConfiguration = local.sfn_network_configuration

              Overrides = {
                ContainerOverrides = [{
                  Name    = "${var.project}-${var.env}-prepare"
                  Command = ["python", "-m", "jobs.prepare.anchors.assemble"]
                }]
              }
            }
            Next = "AnchorsBuildFeatures"
          }

          # ---------------------------------
          # [ANCHORS][PREPARE][FEATURES]
          # ---------------------------------

          AnchorsBuildFeatures = {
            Type     = "Task"
            Resource = "arn:aws:states:::ecs:runTask.sync"
            Parameters = {
              Cluster              = module.compute.ecs_cluster_arn
              LaunchType           = "FARGATE"
              TaskDefinition       = module.tasks.task_definition_arns["prepare"]
              NetworkConfiguration = local.sfn_network_configuration

              Overrides = {
                ContainerOverrides = [{
                  Name    = "${var.project}-${var.env}-prepare"
                  Command = ["python", "-m", "jobs.prepare.anchors.build_features"]
                }]
              }
            }
            End = true
          }
        }
      })
    }

    # ---------------------------------
    # [BASELINE][TRAIN]
    # ---------------------------------

    baseline_train = {
      definition = jsonencode({
        StartAt = "TrainBaseline"
        States = {

          TrainBaseline = {
            Type     = "Task"
            Resource = "arn:aws:states:::ecs:runTask.sync"
            Parameters = {
              Cluster              = module.compute.ecs_cluster_arn
              LaunchType           = "FARGATE"
              TaskDefinition       = module.tasks.task_definition_arns["train"]
              NetworkConfiguration = local.sfn_network_configuration

              Overrides = {
                ContainerOverrides = [{
                  Name    = "${var.project}-${var.env}-train"
                  Command = ["python", "-m", "jobs.train.run", "--config", "configs/train/baseline.json"]
                }]
              }
            }
            End = true
          }
        }
      })
    }

    # ---------------------------------
    # [BASELINE][SELECT]
    # ---------------------------------
    baseline_select = {
      definition = jsonencode({
        StartAt = "SelectBaselineChampion"
        States = {

          SelectBaselineChampion = {
            Type     = "Task"
            Resource = "arn:aws:states:::ecs:runTask.sync"
            Parameters = {
              Cluster              = module.compute.ecs_cluster_arn
              LaunchType           = "FARGATE"
              TaskDefinition       = module.tasks.task_definition_arns["select"]
              NetworkConfiguration = local.sfn_network_configuration

              Overrides = {
                ContainerOverrides = [{
                  Name    = "${var.project}-${var.env}-select"
                  Command = ["python", "-m", "jobs.select.run", "--config", "configs/select/baseline.json"]
                }]
              }
            }
            End = true
          }
        }
      })
    }
  }
}

# ========================================
# Scheduler
# ========================================

module "scheduler" {
  source = "../../modules/scheduler"

  project = var.project
  env     = var.env

  state_machine_arns = module.orchestration.state_machine_arns

  schedules = {
    anchors = {
      machine             = "anchors_prepare"
      schedule_expression = "cron(0 12 2 * ? *)"
    }
  }
}