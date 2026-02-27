output "svc_sg_id" { value = aws_security_group.svc.id }
output "db_sg_id"  { value = aws_security_group.db.id }