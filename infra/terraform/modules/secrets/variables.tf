variable "project" {
    type = string
}

variable "env" {
    type = string
}

variable "values" {
    description = "Map of KEY secret string value"
    type = map(string)
}