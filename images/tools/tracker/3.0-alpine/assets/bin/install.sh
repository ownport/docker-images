#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation

# Install required components
deploy-utils.sh install "tracker"

# Cleanup procedure
deploy-utils.sh cleanup
