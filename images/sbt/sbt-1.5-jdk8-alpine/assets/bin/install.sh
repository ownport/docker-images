#!/bin/sh

set -eu

SBT_VERSION=1.5.5
SBT_DOWNLOAD_URL="https://github.com/sbt/sbt/releases/download/v${SBT_VERSION}/sbt-${SBT_VERSION}.tgz"


# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "bash"
deploy-utils.sh install-build-deps "wget"

echo "[INFO] Installing sbt-${SBT_VERSION}" && \
    wget --progress=dot:giga ${SBT_DOWNLOAD_URL} -O /tmp/sbt.tgz && \
    tar -xzf /tmp/sbt.tgz -C /tmp && \
    mv /tmp/sbt /opt/sbt && \
    ln -s /opt/sbt/bin/sbt /usr/bin/sbt

# Cleanup procedure
deploy-utils.sh cleanup
