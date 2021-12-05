#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "zsh jq"
deploy-utils.sh install "py3-lxml py3-requests py3-beautifulsoup4 py3-yaml" 
deploy-utils.sh install "py3-pytest py3-pytest-cov py3-pytest-xdist py3-pytest-benchmark"

py3-utils.sh install "parsel" 

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
