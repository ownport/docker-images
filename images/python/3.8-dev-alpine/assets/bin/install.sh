#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install-build-deps "py3-wheel"

py3-utils.sh install "pylint==2.5.3"
py3-utils.sh install "pytest==5.4.3 pytest-cov==2.10.0 pytest-xdist==1.33.0 pytest-benchmark==3.2.3"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
