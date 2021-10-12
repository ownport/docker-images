#!/bin/sh

set -eu

GITLAB_CREDS=$(echo -n ${CI_REGISTRY_USER}:${CI_REGISTRY_PASSWORD} | base64 | tr -d '\n')

echo "
{
    \"auths\":{
        \"$CI_REGISTRY\":{
            \"auth\":\"$GITLAB_CREDS\"
        }
    }
}" > /kaniko/.docker/config.json

