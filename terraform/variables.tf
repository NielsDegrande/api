variable "project_id" {
  type    = string
  default = "template-123456"
}

variable "project_number" {
  type    = string
  default = "1234567890"
}

variable "region" {
  type    = string
  default = "europe-west1"
}

variable "location" {
  type    = string
  default = "europe-west1"
}

variable "name" {
  type    = string
  default = "template"
}

variable "image_name" {
  type    = string
  default = "europe-west1-docker.pkg.dev/template-123456/template/api"
}

variable "api_hash" {
  type = string
}

variable "gcp_credentials_path" {
  type    = string
  default = ".secrets/application_default_credentials.json"
}

variable "db_user" {
  type    = string
  default = "postgres"
}

variable "db_password" {
  type = string
}
