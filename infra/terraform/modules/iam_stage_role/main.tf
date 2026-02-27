terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# ----------------------------------------------------------
# Locals
# ----------------------------------------------------------

locals {
  name_prefix = "${var.project}-${var.env}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  ssm_path_arn = "arn:aws:ssm:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:parameter${trimprefix(var.ssm_read_path_prefix, "/")}/*"
}

# ----------------------------------------------------------
# Policy Document
# ----------------------------------------------------------

data "aws_iam_policy_document" "stage" {

  # --------------------------
  # S3 Read
  # --------------------------
  dynamic "statement" {
    for_each = length(var.s3_read_bucket_arns) > 0 ? [1] : []
    content {
      sid     = "S3ListBuckets"
      effect  = "Allow"
      actions = ["s3:ListBucket"]
      resources = var.s3_read_bucket_arns
    }
  }

  dynamic "statement" {
    for_each = length(var.s3_read_bucket_arns) > 0 ? [1] : []
    content {
      sid     = "S3GetObjects"
      effect  = "Allow"
      actions = ["s3:GetObject"]
      resources = [
        for b in var.s3_read_bucket_arns : "${b}/*"
      ]
    }
  }

  # --------------------------
  # S3 Write
  # --------------------------
  dynamic "statement" {
    for_each = length(var.s3_write_bucket_arns) > 0 ? [1] : []
    content {
      sid     = "S3WriteObjects"
      effect  = "Allow"
      actions = ["s3:PutObject"]
      resources = [
        for b in var.s3_write_bucket_arns : "${b}/*"
      ]
    }
  }

  # --------------------------
  # SSM Read (by path)
  # --------------------------
  statement {
    sid     = "SSMReadByPath"
    effect  = "Allow"
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:GetParametersByPath"
    ]
    resources = [local.ssm_path_arn]
  }

  # --------------------------
  # SSM Write
  # --------------------------
  dynamic "statement" {
    for_each = length(var.ssm_write_parameter_arns) > 0 ? [1] : []
    content {
      sid     = "SSMWriteParameters"
      effect  = "Allow"
      actions = ["ssm:PutParameter"]
      resources = var.ssm_write_parameter_arns
    }
  }

  # --------------------------
  # Secrets Read
  # --------------------------
  dynamic "statement" {
    for_each = length(var.secrets_read_secret_arns) > 0 ? [1] : []
    content {
      sid     = "SecretsRead"
      effect  = "Allow"
      actions = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      resources = var.secrets_read_secret_arns
    }
  }
}

# ----------------------------------------------------------
# IAM Policy
# ----------------------------------------------------------

resource "aws_iam_policy" "stage" {
  name   = "${local.name_prefix}-${var.role_name}-policy"
  policy = data.aws_iam_policy_document.stage.json
}

# ----------------------------------------------------------
# IAM Role
# ----------------------------------------------------------

resource "aws_iam_role" "task" {
  name               = "${local.name_prefix}-${var.role_name}"
  assume_role_policy = local.assume_role_policy
}

# ----------------------------------------------------------
# Attach Policy
# ----------------------------------------------------------

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.task.name
  policy_arn = aws_iam_policy.stage.arn
}