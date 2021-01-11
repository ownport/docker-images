#!/bin/sh

set -eu

NODEJS_VERSION="12.18.4"
NODEJS_CHECKSUM="99715657ad621bd364070f176d27c6902ce49441af88e5df2dbe63392a3097da"
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

# Cleanup procedure
deploy-utils.sh cleanup

echo '[INFO] Run smoke tests' && \
    echo 'node version: ' $(node --version) && \
    echo 'npm version: ' $(npm --version) && \
    echo 'npx version: ' $(npx --version)

