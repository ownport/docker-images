#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "python3 py3-pip"
ln -s /usr/bin/python3.9 /usr/bin/python

# Cleanup procedure
deploy-utils.sh cleanup
py3-utils.sh cleanup
