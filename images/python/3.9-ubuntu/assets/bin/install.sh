#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

echo "[INFO] Install py3-utils script" && \
    mv /tmp/assets/bin/py3-utils.sh /usr/local/bin/ && \

# Installation
# deploy-utils.sh install "apt-utils"
deploy-utils.sh install "python3 python3-pip"

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
