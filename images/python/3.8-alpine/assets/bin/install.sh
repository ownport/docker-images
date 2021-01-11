#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "python3=3.8.5-r0 py3-pip"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
