#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "bash jq"
deploy-utils.sh install "libxml2 libxslt"

BUILD_DEPS="py3-wheel gcc musl-dev python3-dev build-base libxml2-dev libxslt-dev libffi-dev openssl-dev"
deploy-utils.sh install-build-deps ${BUILD_DEPS}

py3-utils.sh install "scrapy==2.2.1"
py3-utils.sh install "PyYAML==5.3.1" 

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
