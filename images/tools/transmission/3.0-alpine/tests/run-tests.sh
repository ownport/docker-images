#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Checking transmission-cli version' && \
    echo 'transmission-cli version: ' $(transmission-cli --version) 

echo "[INFO] Tests were completed"
