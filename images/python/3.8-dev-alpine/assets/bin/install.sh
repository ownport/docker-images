#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install-build-deps "py3-wheel"

py3-utils.sh install "pylint"
py3-utils.sh install "pytest pytest-cov pytest-xdist pytest-benchmark"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
