#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
py3-utils.sh install "luigi"

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
