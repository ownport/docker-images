#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "rust cargo"

# Cleanup procedure
deploy-utils.sh cleanup
