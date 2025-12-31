terraform {
    required_version = ">= 1.5.0"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = ">= 5.0"
        }
    }
}

provider "aws" {
    region = "us-east-1"
    profile = "nowcasting-dev"
}

# Pattern: <project>-<env>-<resource>-<region>
resource "aws_s3_bucket" "data" {
    bucket = "e2e-macro-nowcasting-dev-data-us-east-1"
}

resource "aws_s3_bucket" "artifacts" {
    bucket = "e2e-macro-nowcasting-dev-artifacts-us-east-1"
}

# safety: block public access
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

output "data_bucket" {
    value = aws_s3_bucket.data.bucket
}

output "artifacts_bucket" {
    value = aws_s3_bucket.artifacts.bucket
}