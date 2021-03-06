#!/bin/sh

set -eu

# Environment variables
T_USER=transmission
T_USER_ID=1000
T_GROUP=transmission
T_GROUP_ID=1000

# Preparation
deploy-utils.sh update

# Installation

# Install builde dependencies
deploy-utils.sh install-build-deps "curl"

# Add user and group
deploy-utils.sh add-user-and-group \
    ${T_USER_ID} ${T_USER} ${T_GROUP_ID} ${T_GROUP}

# Install required components
deploy-utils.sh install "transmission-cli transmission-daemon"
deploy-utils.sh install "ca-certificates" && \
    update-ca-certificates

# Create configuration
echo '[INFO] Creating transmission configuration' && \
    mkdir -p \
        /etc/transmission \
        /transmission/downloads \
        /transmission/incomplete && \
    mv /tmp/assets/conf/settings.json /etc/transmission/ && \
    chown -R ${T_USER_ID}:${T_GROUP_ID} \
        /transmission /etc/transmission

# Cleanup procedure
deploy-utils.sh cleanup
