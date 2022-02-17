#!/bin/sh

set -eu
    
# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "prometheus"

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

# Cleanup procedure
deploy-utils.sh cleanup