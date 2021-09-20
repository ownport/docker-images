#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "bazel4"

# Cleanup procedure
deploy-utils.sh cleanup


