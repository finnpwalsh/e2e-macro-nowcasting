terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

# ---------------
# Provider
# ---------------

provider "aws" {
  region = var.aws_region
}

# ---------------
# Locals
# ---------------

locals {
  data_bucket_name         = "${var.project}-${var.env}-data-${var.aws_region}"
  artifacts_bucket_name    = "${var.project}-${var.env}-artifacts-${var.aws_region}"
  airflow_logs_bucket_name = "${var.project}-${var.env}-airflow-logs-${var.aws_region}"
}

# ---------------
# S3 Buckets
# ---------------

resource "aws_s3_bucket" "data" {
  bucket = local.data_bucket_name
}

resource "aws_s3_bucket" "artifacts" {
  bucket = local.artifacts_bucket_name
}

resource "aws_s3_bucket" "airflow_logs" {
  bucket = local.airflow_logs_bucket_name
}

# ---------------
# Access Blocks
# ---------------

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket                  = aws_s3_bucket.artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "airflow_logs" {
  bucket                  = aws_s3_bucket.airflow_logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}