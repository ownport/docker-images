#!/bin/sh

set -eu

GITLAB_CREDS=$(echo -n ${CI_REGISTRY_USER}:${CI_REGISTRY_PASSWORD} | base64 | tr -d '\n')

echo "[INFO] Creating directory, /kaniko/.docker" && \
    mkdir -p /kaniko/.docker

echo "[INFO] Updating kaniko docker config" && \
echo "
{
    \"auths\":{
        \"$CI_REGISTRY\":{
            \"auth\":\"$GITLAB_CREDS\"
        }
    }
}" > /kaniko/.docker/config.json

