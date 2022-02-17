#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
# deploy-utils.sh install "libstdc++ openblas"
deploy-utils.sh install "bash jq"
# deploy-utils.sh install-build-deps "py3-wheel gcc cython python3-dev openblas-dev build-base"

# py3-utils.sh install "numpy==1.22.0" 
# py3-utils.sh install "scipy==1.8.0"
# py3-utils.sh install "scikit-learn==1.0.2"

py3-utils.sh install "pandas==1.4.1"
py3-utils.sh install "ipython==8.0.1"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
