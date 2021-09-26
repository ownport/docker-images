#!/bin/sh

set -eu

# Versions
DOCKER_VERSION="20.10.8"

# Preparation
deploy-utils.sh update

# Install required packages for builder
deploy-utils.sh install "python3 git"

deploy-utils.sh install-build-deps "wget tar"
echo "[INFO] Install docker tools" && \
    wget --no-check-certificate --progress=dot:giga \
        -O /tmp/docker.tgz \
        https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz && \
    tar --extract \
        --file /tmp/docker.tgz \
        --strip-components 1 \
        --directory /usr/local/bin/ && \
    rm /tmp/docker.tgz

# Cleanup procedure
deploy-utils.sh cleanup
