#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "podman=3.2.3"

# Cleanup procedure
deploy-utils.sh cleanup
