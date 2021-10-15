#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "sudo"

# VS Code User
USER_ID="1000"
USER_NAME="vscode"
GROUP_ID="1000"
GROUP_NAME="vscode"

deploy-utils.sh add-user-and-group \
    ${USER_ID} ${USER_NAME} \
    ${GROUP_ID} ${GROUP_NAME} \
    /bin/zsh

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
