#!/bin/sh

set -eu

echo "[INFO] Install py3-utils script" && \
    mv /tmp/assets/bin/py3-utils.sh /usr/local/bin/ && \
    
# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "python3 py3-pip"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
