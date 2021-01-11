#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "libstdc++ openblas"
deploy-utils.sh install "bash jq"
deploy-utils.sh install-build-deps "py3-wheel gcc musl-dev cython python3-dev openblas-dev build-base"

py3-utils.sh install "numpy==1.19.0" 
py3-utils.sh install "scipy==1.5.1"
py3-utils.sh install "scikit-learn==0.23.0"

py3-utils.sh install "pandas==1.0.5"
py3-utils.sh install "ipython==7.16.1"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
