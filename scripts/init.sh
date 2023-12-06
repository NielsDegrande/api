#!/bin/sh
# Initialize deploy.

# Login and authenticate with Google.
gcloud auth application-default login
gcloud auth configure-docker europe-west1-docker.pkg.dev

(
  cd terraform || exit
  terraform init
)
