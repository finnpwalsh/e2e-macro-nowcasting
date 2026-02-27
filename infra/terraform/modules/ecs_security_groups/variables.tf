variable "project" { type = string }
variable "env"     { type = string }
variable "vpc_id"  { type = string }

variable "ui_ingress_cidrs" {
    type = list(string)
    description = "CIDRs allowed to access Airflow/MLflow UIs"
}