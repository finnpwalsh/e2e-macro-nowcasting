resource "random_password" "this" {
  length  = 24
  special = true
}

# ------------------------------------------------------------
# Subnet group
# ------------------------------------------------------------

resource "aws_db_subnet_group" "this" {
    name = "${var.project}-${var.env}-rds-subnets"
    subnet_ids = var.subnet_ids
}

# ------------------------------------------------------------
# Security group
# ------------------------------------------------------------

resource "aws_security_group" "this" {
    name        = "${var.project}-${var.env}-rds-sg"
    description = "RDS Postgres access"
    vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "ingress_from_ecs" {
    type                     = "ingress"
    security_group_id        = aws_security_group.this.id
    from_port                = 5432
    to_port                  = 5432
    protocol                 = "tcp"
    source_security_group_id = var.allowed_sg_id
}

resource "aws_security_group_rule" "egress_all" {
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
    identifier = "${var.project}-${var.env}-postgres"

    engine         = "postgres"
    engine_version = var.engine_version

    instance_class    = var.instance_class
    allocated_storage = var.allocated_storage

    db_name  = var.db_name
    username = var.username
    password = random_password.this.result
    port     = 5432

    db_subnet_group_name   = aws_db_subnet_group.this.name
    vpc_security_group_ids = [aws_security_group.this.id]

    publicly_accessible = false

    skip_final_snapshot = true
    deletion_protection = false
}

# ------------------------------------------------------------
# Secret version
# ------------------------------------------------------------

resource "aws_secretsmanager_secret_version" "airflow_db_uri" {
  secret_id = var.secrets["AIRFLOW_DB_URI"]
  secret_string = "postgresql+psycopg2://${var.username}:${random_password.this.result}@${aws_db_instance.this.address}:${aws_db_instance.this.port}/airflow"
}

resource "aws_secretsmanager_secret_version" "mlflow_backend_store_uri" {
  secret_id = var.secrets["MLFLOW_BACKEND_STORE_URI"]
  secret_string = "postgresql://${var.username}:${random_password.this.result}@${aws_db_instance.this.address}:${aws_db_instance.this.port}/mlflow"
}