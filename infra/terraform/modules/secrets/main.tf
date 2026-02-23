locals {
    base = "/${var.project}/${var.env}/secrets"
}

resource "aws_secretsmanager_secret" "this" {
    for_each = var.keys

    name = "${local.base}/${each.key}"
    description = "Managed by Terraform (${var.project}/${var.env})"
}