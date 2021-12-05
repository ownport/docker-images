#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[INFO] Print out uname' && \
    uname -a

echo 'node version: ' $(node --version)
echo 'npm version: ' $(npm --version)
echo 'npx version: ' $(npx --version)
