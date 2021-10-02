#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "python3=3.8.2-0ubuntu2 python3-pip"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
