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

  runtimes_norm = {
    for k, v in var.runtimes : k => merge(v, {
      ssm_path_arn = "arn:aws:ssm:${var.aws_region}:${var.aws_account_id}:parameter/${trim(v.ssm_read_path_prefix, "/")}/*"
    })
  }
}

# ----------------------------------------------------------
# ECR Repos
# ----------------------------------------------------------

resource "aws_ecr_repository" "runtime" {
  for_each = local.runtimes_norm
  name                 = "${local.name_prefix}-${each.key}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# ----------------------------------------------------------
# CloudWatch Log Groups
# ----------------------------------------------------------

resource "aws_cloudwatch_log_group" "runtime" {
  for_each = local.runtimes_norm

  name              = "/ecs/${local.name_prefix}/${each.key}"
  retention_in_days = var.log_retention_days
}

# ----------------------------------------------------------
# Policy Document
# ----------------------------------------------------------

data "aws_iam_policy_document" "runtime" {
  for_each = local.runtimes_norm

  # --------------------------
  # S3 Read
  # --------------------------
  dynamic "statement" {
    for_each = length(each.value.s3_read_bucket_arns) > 0 ? [1] : []
    content {
      sid     = "S3ListBuckets"
      effect  = "Allow"
      actions = ["s3:ListBucket"]
      resources = each.value.s3_read_bucket_arns
    }
  }

  dynamic "statement" {
    for_each = length(each.value.s3_read_bucket_arns) > 0 ? [1] : []
    content {
      sid     = "S3GetObjects"
      effect  = "Allow"
      actions = ["s3:GetObject"]
      resources = [
        for b in each.value.s3_read_bucket_arns : "${b}/*"
      ]
    }
  }

  # --------------------------
  # S3 Write
  # --------------------------
  dynamic "statement" {
    for_each = length(each.value.s3_write_bucket_arns) > 0 ? [1] : []
    content {
      sid     = "S3WriteObjects"
      effect  = "Allow"
      actions = ["s3:PutObject"]
      resources = [
        for b in each.value.s3_write_bucket_arns : "${b}/*"
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
      "ssm:GetParametersByPath"
    ]
    resources = [each.value.ssm_path_arn]
  }

  # --------------------------
  # SSM Write
  # --------------------------
  dynamic "statement" {
    for_each = length(each.value.ssm_write_parameter_arns) > 0 ? [1] : []
    
    content {
      sid     = "SSMWriteParameters"
      effect  = "Allow"
      actions = ["ssm:PutParameter"]
      resources = each.value.ssm_write_parameter_arns
    }
  }

  # --------------------------
  # Secrets Read
  # --------------------------
  dynamic "statement" {
    for_each = length(each.value.secrets_read_secret_arns) > 0 ? [1] : []
    
    content {
      sid     = "SecretsRead"
      effect  = "Allow"
      actions = [
        "secretsmanager:GetSecretValue",
      ]
      resources = each.value.secrets_read_secret_arns
    }
  }
}

# ----------------------------------------------------------
# IAM Policy
# ----------------------------------------------------------

resource "aws_iam_policy" "runtime" {
  for_each = local.runtimes_norm
  
  name   = "${local.name_prefix}-${each.key}-policy"
  policy = data.aws_iam_policy_document.runtime[each.key].json
}

# ----------------------------------------------------------
# IAM Role
# ----------------------------------------------------------

resource "aws_iam_role" "runtime" {
  for_each = local.runtimes_norm
  name               = "${local.name_prefix}-${each.key}"
  assume_role_policy = local.assume_role_policy
}

# ----------------------------------------------------------
# Attach Policy
# ----------------------------------------------------------

resource "aws_iam_role_policy_attachment" "attach" {
  for_each   = local.runtimes_norm
  role       = aws_iam_role.runtime[each.key].name
  policy_arn = aws_iam_policy.runtime[each.key].arn
}