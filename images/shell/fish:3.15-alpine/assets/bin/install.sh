#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "fish"

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

# Cleanup procedure
deploy-utils.sh cleanup
