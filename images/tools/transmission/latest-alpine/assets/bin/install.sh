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

# Create configuration
echo '[INFO] Creating configuration' && \
    mkdir -p \
        /etc/transmission \
        /transmission/downloads \
        /transmission/incomplete && \
    mv /tmp/assets/conf/settings.json /etc/transmission/ && \
    chown -R ${T_USER_ID}:${T_GROUP_ID} \
        /transmission /etc/transmission

# Cleanup procedure
deploy-utils.sh cleanup

echo '[INFO] Run smoke tests' && \
    echo 'transmission-cli version: ' $(transmission-cli --version) 
