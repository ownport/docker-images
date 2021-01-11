#!/bin/sh

set -eu

SCALA_VERSION=2.13.3
SCALA_DOWNLOAD_URL=https://downloads.lightbend.com/scala/${SCALA_VERSION}/scala-${SCALA_VERSION}.tgz


# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "bash"
deploy-utils.sh install-build-deps "wget"

echo "[INFO] Installing Scala-${SCALA_VERSION}" && \
    wget --progress=dot:giga ${SCALA_DOWNLOAD_URL} -O /tmp/scala.tgz && \
    tar -xzf /tmp/scala.tgz -C /tmp #&& \
    mv /tmp/scala-${SCALA_VERSION} /opt/scala && \
    ln -s /opt/scala/bin/scala /usr/bin/scala &&
    ln -s /opt/scala/bin/scalac /usr/bin/scalac &&

# Cleanup procedure
deploy-utils.sh cleanup

echo "[INFO] Basic smoke tests" && \
    java -version && \
    javac -version && \
    scala --version && \
    scalac --version

