#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install-build-deps "g++ unzip zip"



# Cleanup procedure
deploy-utils.sh cleanup


