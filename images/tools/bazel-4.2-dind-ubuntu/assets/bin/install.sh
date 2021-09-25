#!/bin/sh

set -eu

# Versions
DOCKER_VERSION="20.10.8"

# Preparation
deploy-utils.sh update

echo "[INFO] Install docker tools" && \
    curl https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz \
        -o /tmp/docker.tgz && \
    tar --extract \
        --file /tmp/docker.tgz \
        --strip-components 1 \
        --directory /usr/local/bin/ && \
    rm /tmp/docker.tgz

echo "[INFO] Install dind tool" && \
    curl https://raw.githubusercontent.com/moby/moby/20.10/hack/dind \
        -o /usr/local/bin/dind && \
    chmod +x /usr/local/bin/dind

# Cleanup procedure
deploy-utils.sh cleanup


