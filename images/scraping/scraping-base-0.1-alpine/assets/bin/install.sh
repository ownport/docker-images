#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "zsh jq"
deploy-utils.sh install "libxml2 libxslt"

deploy-utils.sh install-build-deps "py3-wheel gcc musl-dev python3-dev build-base libxml2-dev libxslt-dev"

py3-utils.sh install "requests==2.24.0"
py3-utils.sh install "lxml==4.5.2" 
py3-utils.sh install "parsel==1.6.0" 
py3-utils.sh install "beautifulsoup4==4.9.1"
py3-utils.sh install "PyYAML==5.3.1" 

py3-utils.sh install "pytest==5.4.3 pytest-cov==2.10.0 pytest-xdist==1.33.0 pytest-benchmark==3.2.3"

echo "[INFO] Running smoke tests" && \
    /tmp/assets/tests/smoke-tests.sh

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
