#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Build dependencies
deploy-utils.sh install-build-deps "gcc python3-dev musl-dev libffi-dev"

# Installation
deploy-utils.sh install "git jq make zsh bash zip"
deploy-utils.sh install "py3-wheel py3-setuptools py3-cryptography"

# Build and deploy
py3-utils.sh install "twine build"
py3-utils.sh install "setuptools_scm[toml]>=3.4"

# Python Tools
py3-utils.sh install "pip-tools"

# Git Tools
py3-utils.sh install "pre-commit"

# Linters
py3-utils.sh install "pylint"

# Testing
py3-utils.sh install "coverage[toml]"
py3-utils.sh install "pytest pytest-cov pytest-xdist pytest-benchmark pytest-mock"

# Update scripts
if [ -d /tmp/assets/bin/dev/ ] ; then
    echo '[INFO] Update dev scripts'
    mkdir -p /usr/local/bin/dev/
    SCRIPTS="cleanup.sh release.sh run-pytest.sh publish.sh"
    for script in ${SCRIPTS}; do
        mv /tmp/assets/bin/dev/${script} /usr/local/bin/dev/${script}
    done
else
    echo "[WARNING] Missing the directory: /tmp/assets/bin/dev/"
fi

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
