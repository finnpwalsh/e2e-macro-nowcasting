# ========================================
# SVC
# ========================================

resource "aws_security_group" "svc" {
    name = "${var.project}-{var.env}-svc-sg"
    vpc_id = var.vpc_id

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_security_group_rule" "svc_airflow_ui" {
    type              = "ingress"
    security_group_id = aws_security_group.svc.id
    from_port         = 8080
    to_port           = 8080
    protocol          = "tcp"
    cidr_blocks       = var.ui_ingress_cidrs
}

resource "aws_security_group_rule" "svc_airflow_ui" {
    type              = "ingress"
    security_group_id = aws_security_group.svc.id
    from_port         = 5000
    to_port           = 5000
    protocol          = "tcp"
    cidr_blocks       = var.ui_ingress_cidrs
}

# ========================================
# DB
# ========================================

resource "aws_security_group" "db" {
    name = "${var.project}-${var.env}-db-sg"
    vpc_id = var.vpc_id

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_security_group_rule" "db_from_svc" {
    type                     = "ingress"
    security_group_id        = aws_security_group.db.id
    from_port                = 5432
    to_port                  = 5432
    protocol                 = "tcp"
    source_security_group_id = aws_security_group.svc.id
}