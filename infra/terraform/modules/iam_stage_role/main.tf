terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = ">= 5.0"
        }
    }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
    name_prefix = "${var.project}-${var.env}"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [{
            Effect = "Allow"
            Principal = { Service = "ecs-tasks.amazonaws.com"}
            Action = "sts:AssumeRole"
        }]
    })

    ssm_path_arn = "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter${trimprefix(var.ssm_read_path_prefix,, "/)}*"
}

resource "aws_iam_role" "task" {
    name = "${local.name_prefix}-${var.role_name}"
    assume_role_policy = local.assume_role_policy
}

resource "aws_iam_policy" "stage" {
    name = "${local.name_prefix}-${var.role_name}-policy"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            # S3 Read
            {
                Sid = "S3ListBuckets"
                Effect = "Allow"
                Action = ["s3:ListBucket"]
                Resource = var.s3_read_bucket_arns
            },
            {
                Sid = "S3GetObjects"
                Effect = "Allow"
                Action = ["s3:GetObject"]
                Resource = [for b in var.s3_read_bucket_arns : "${b}/*"]
            },
            # S3 Write
            {
                Sid = "S3WriteObjects"
                Effect = "Allow"
                Action = ["s3:PutObject"]
                Resource = [for b in var.s3_write_bucket_arns : "${b}/*"]
            }
            # SSM Read
            {
                Sid = "SSMReadByPath"
                Effect = "Allow"
                Action = [
                    "ssm:GetParameter",
                    "ssm:GetParameters",
                    "ssm:GetParametersByPath"
                ]
                Resource = local.ssm_path_arn
            },
            # SSM Write
            {
                Sid = "SSMWriteParameters"
                Effect = "Allow"
                Action = ["ssm:PutParameter"]
                Resource = var.ssm_write_parameter_arns
            }
            # Secrets Read
            {
                Sid = "SecretsRead"
                Effect = "Allow"
                Action = [
                    "secretsmanager:GetSecretValue",
                    "secretsmanager:DescribeSecret"
                ]
                Resource = var.secrets_read_secret_arns
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "attach" {
    role = aws_iam_role.task.name
    policy_arn = aws_iam_policy.stage.arn
}