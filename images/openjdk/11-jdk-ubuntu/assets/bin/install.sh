#!/bin/sh

set -eu

# removing extra files
cleanup() {

    echo "[INFO] Cleaning extra files" && \
        rm -rf \
            /usr/share/X11 \
            /usr/lib/jvm/java-11-openjdk-amd64/man \
            /usr/lib/jvm/java-11-openjdk-amd64/demo \
            /usr/lib/jvm/java-11-openjdk-amd64/jmods/java.desktop.* \
            /usr/lib/jvm/java-11-openjdk-amd64/jmods/jdk.unsupported.desktop.jmod
}

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "openjdk-11-jdk-headless"

# Cleanup procedure
cleanup
deploy-utils.sh cleanup




