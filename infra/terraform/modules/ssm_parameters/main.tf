locals {
    base = "/${var.project}/${var.env}/config"
}

resource "aws_ssm_parameters" "this" {
    for_each = var.values

    name = "${local.base}/{each.key}"
    type = "String"
    value = each.value
    overwrite = true
}