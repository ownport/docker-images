#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "zsh jq"

# Python dependencies
deploy-utils.sh install "py3-cryptography py3-lxml py3-yaml"

# Install Scrapy
py3-utils.sh install "Scrapy==2.5.1"

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
