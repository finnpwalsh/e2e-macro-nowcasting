# ------------------------------------------------------------
# Subnet group
# ------------------------------------------------------------

resource "aws_db_subnet_group" "this" {
    name = "${var.project}-${var.env}-rds-subnets"
    subnet_ids = var.private_subnet_ids
}

# ------------------------------------------------------------
# Security group
# ------------------------------------------------------------

resource "aws_security_group" "this" {
    name        = "${var.project}-${var.env}-rds-sg"
    description = "RDS Postgres access"
    vpc_id      = var.vpc_id
}

resource "aws_security_group_role" "ingress_from_ecs" {
    type                     = "ingress"
    security_group_id        = aws_security_group.this.id
    from_port                = 5432
    to_port                  = 5432
    protocol                 = "tcp"
    source_security_group_id = var.allowed_sg_id
}

resource "aws_security_group_role" "egress_all" {
    type              = "egress"
    security_group_id = aws_security_group.this.id
    from_port         = 0
    to_port           = 0
    protocol          = "-1"
    cidr_blocks       = ["0.0.0.0/0"]
}

# ------------------------------------------------------------
# RDS instance
# ------------------------------------------------------------
resource "aws_db_instance" "this" {
    identifier = "${var.project}-${var.env}-postgres

    engine         = "postgres"
    engine_version = var.engine_version

    port = 5432

    db_subnet_group_name   = aws_db_subnet_group.this.name
    vpc_security_group_ids = [aws.security_group.this.id]

    publicly_accessible = false

    skip_final_snapshot = true
    deletion_protection = false
}