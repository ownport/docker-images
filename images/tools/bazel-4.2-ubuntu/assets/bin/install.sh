#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update
deploy-utils.sh install-build-deps "curl gnupg"

curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg && \
    mv bazel.gpg /etc/apt/trusted.gpg.d/

echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | \
    tee /etc/apt/sources.list.d/bazel.list

deploy-utils.sh update

# Installation
deploy-utils.sh install "bazel"

# Cleanup procedure
deploy-utils.sh cleanup


