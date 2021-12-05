#!/bin/sh

set -eu

NODEJS_VERSION="12.22.6"
NODEJS_CHECKSUM="0ce2b97ecbbd84f1a5ed13278ed6845d93c6454d8550730b247a990438dba322"
NODEJS_DIST_URL="https://unofficial-builds.nodejs.org/download/release/v$NODEJS_VERSION/node-v$NODEJS_VERSION-linux-x64-musl.tar.xz"

# Preparation
deploy-utils.sh update

# Installation

# Install builde dependencies
deploy-utils.sh install-build-deps "curl"

# Install required components
deploy-utils.sh install "libstdc++"

# Download NodeJS package
echo "[INFO] Downloading NodeJS package, ${NODEJS_DIST_URL}" && \
    curl --progress-bar -o /tmp/nodejs.tar.xz ${NODEJS_DIST_URL} && \
    echo "${NODEJS_CHECKSUM}  /tmp/nodejs.tar.xz" | sha256sum -c - && \
    mkdir -p /opt/nodejs && \
    tar -xJf /tmp/nodejs.tar.xz -C /opt/nodejs --strip-components=1 && \
    ln -s /opt/nodejs/bin/node /usr/local/bin/node && \
    ln -s /opt/nodejs/bin/npm /usr/local/bin/npm && \
    ln -s /opt/nodejs/bin/npx /usr/local/bin/npx

# Add user and group
deploy-utils.sh add-user-and-group 1000 node 1000 node

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

# Cleanup procedure
deploy-utils.sh cleanup

