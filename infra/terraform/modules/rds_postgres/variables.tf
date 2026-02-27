variable "project" { type = string }
variable "env"     { type = string }

variable "vpc_id"  { type = string }
variable "subnet_ids" { type = list(string) }

variable "allowed_sg_id" { type = string }

variable "db_name" { type = string, default = "postgres" }
variable "username" { type = string, default = "nowcasting" }
variable "password" { type = string, sensitive = true }

variable "instance_class" { type = string, default = "db.t4g.micro" }
variable "allocated_storage" { type = number, default = 20 }
variable "engine_version"    { type = string, defauly = "16.3" }