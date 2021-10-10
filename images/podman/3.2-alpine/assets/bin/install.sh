#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "podman"

# Cleanup procedure
deploy-utils.sh cleanup
