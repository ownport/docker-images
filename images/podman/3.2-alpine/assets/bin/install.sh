#!/bin/sh

set -eu

# Preparation
deploy-utils.sh update

# Installation
deploy-utils.sh install "podman=3.2.3-r1"

# Configure user and group
deploy-utils.sh add-user-and-group 1000 podman 1000 podman

# Since we can run rootfull and rootless containers with this image 
# we create two volumes.  Rootfull Podman uses 
#
#   /var/lib/containers  
#
# for it’s container storage and rootless uses 
#
#   /home/podman/.local/share/containers.  
#
# Overlay over overlay is often denied by the kernel, so this creates 
# non overlay volumes to be used within the container.
echo "[INFO] Create podman directories" && \
    mkdir -p \
        /var/lib/containers \
        /home/podman/.local/share/containers

# Update podman configs
echo "[INFO] Copy containers configs" && \
    mv /tmp/assets/conf/* /etc/containers/


# Cleanup procedure
deploy-utils.sh cleanup
