#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "zsh jq"
deploy-utils.sh install "libxml2 libxslt"

# Python dependencies
deploy-utils.sh install "py3-cryptography py3-lxml"

# Install Scrapy
py3-utils.sh install "Scrapy==2.5.0"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
