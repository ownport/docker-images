#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Install required packages for builder
deploy-utils.sh install "python3 git"

# Cleanup procedure
deploy-utils.sh cleanup
