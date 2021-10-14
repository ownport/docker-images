#!/bin/sh

set -eu

echo "[INFO] Install deploy-utils script" && \
    mv /tmp/assets/bin/py3-utils.sh /usr/local/bin/ && \
    
# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "python3=3.8.2-0ubuntu2 python3-pip"

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
