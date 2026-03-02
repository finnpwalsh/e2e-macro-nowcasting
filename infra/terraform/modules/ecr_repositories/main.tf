resource "aws_ecr_repository" "this" {
    for_each = toset(var.repositories)
    
    name = "${var.project}-${var.env}-${each.key}"
    image_tag_mutability = "MUTABLE"

    image_scanning_configuration { scan_on_push = true}
    force_delete = true
}