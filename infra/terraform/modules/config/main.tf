locals {
    base = "/${var.project}/${var.env}/config"
}

# ----------------------------------------------------------
# SSM Parameters
# ----------------------------------------------------------

resource "aws_ssm_parameter" "config" {
    for_each = var.ssm_parameters

    name = "${local.base}/${each.key}"
    type = string
    value = each.value
}

# ----------------------------------------------------------
# Secrets
# ----------------------------------------------------------

resource "aws_secretsmanager_secret" "secret" {
    for_each = var.secrets

    name = "${var.project}-${var.env}-${each.key}"
}