variable "project" {
    type = string
}

variable "env" {
    type = string
}

variable "keys" {
    description = "Set of secret keys to create"
    type = set(string)
}