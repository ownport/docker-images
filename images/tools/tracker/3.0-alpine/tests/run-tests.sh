#!/bin/sh

set -e

echo "[INFO] Run tests"

echo '[TEST] Checking tracker version' && \
    echo 'tracker version: ' $(tracker --version) 

echo "[INFO] Tests were completed"
