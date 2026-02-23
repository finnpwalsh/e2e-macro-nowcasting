locals {
    base = "/${var.project}/${var.env}/secrets"
}

resource "aws_secretsmanager_secret" "this" {
    for_each = var.values
    name = "${local.base}/${each.key}"
}

resource "aws_secretsmanager_secret_version" "this" {
    for_each = var.values
    secret_id = aws_secretsmanager_secret.this[each.key].id
    secret_string = each.value
}