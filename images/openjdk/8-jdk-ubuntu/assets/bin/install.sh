#!/bin/sh

set -eu

# removing extra files
cleanup() {

    echo "[INFO] Cleaning extra files" && \
        rm -rf \
            /usr/share/X11 \
            /usr/share/fonts \
            /usr/lib/jvm/java-11-openjdk-amd64/man \
            /usr/lib/jvm/java-11-openjdk-amd64/docs \
            /usr/lib/jvm/java-8-openjdk-amd64/jre/man 
}

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "openjdk-8-jdk-headless"

# Cleanup procedure
cleanup
deploy-utils.sh cleanup




