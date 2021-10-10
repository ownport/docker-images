#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "podman=3.2.3-r1"

# Update podman configs
mv /tmp/assets/conf/* /etc/containers/

# Configure user and group
deploy-utils.sh add-user-and-group 1000 podman 1000 podman

# Cleanup procedure
deploy-utils.sh cleanup
