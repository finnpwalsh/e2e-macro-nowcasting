variable "project" {
    type = string
}

variable "env" {
    type = string
}

variable "values" {
    description = "Map of KEY -> value (non-secret config)
    type = map(string)
}