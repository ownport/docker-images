#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "apt-utils"

deploy-utils.sh install "python3"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
