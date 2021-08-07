#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "openjdk8 libc6-compat"
echo "[INFO] Create sym links" && \
    ln -s /usr/lib/jvm/default-jvm/bin/javac /usr/bin/javac && \
    ln -s /lib64/ld-linux-x86-64.so.2 /lib/ld-linux-x86-64.so.2

# Cleanup procedure
deploy-utils.sh cleanup

