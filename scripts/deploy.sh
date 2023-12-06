#!/bin/sh
# Use Terraform to deploy the infrastructure.

TF_VAR_api_hash="$(git rev-parse --short HEAD)"
export TF_VAR_api_hash
export TF_VAR_db_password
(
  cd terraform || exit
  terraform plan
  terraform apply
)
